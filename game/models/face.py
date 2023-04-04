import numpy as np
import glm
import moderngl

from constants.colors import Colors
from engine.vectors import normalize_vector
from engine.renderable import Renderable
from engine.camera import Camera
from engine.shader import get_shader_program
from puzzles.face_generator_definition import FaceGeneratorDefinition
from puzzles.puzzle_node import PuzzleNode
from puzzles.puzzle_face import PuzzleFace
from models.types import Vertex, UV
from models.helpers import merge_collection_items

INACTIVE_LINE_COLOR = Colors.GRAY
LINE_COLOR = Colors.WHITE

DISTANCE_MULTIPLER = 1.01
PUZZLE_PATH_WIDTH = 0.1
RAD60 = np.radians(60)
SIN60 = np.sin(RAD60)

ROTATION_TARGET_ANGLE = 120
ROTATION_DURATION = 250

# This helps us render the lines above the face instead of inside it

class FaceCoordinateSystem:

  def __init__(
    self,
    face_generator_definition: FaceGeneratorDefinition,
    vertex_0,
    vertex_1,
    vertex_2
  ):
    self.face_generator_definition = face_generator_definition
    vertex_m0 = np.multiply(vertex_0, DISTANCE_MULTIPLER)
    vertex_m1 = np.multiply(vertex_1, DISTANCE_MULTIPLER)
    vertex_m2 = np.multiply(vertex_2, DISTANCE_MULTIPLER)

    self.origin_vector = vertex_m0

    self.u_vector = np.subtract(vertex_m1, vertex_m0)
    u_vector_mag = np.linalg.norm(self.u_vector)

    self.normal_vector = normalize_vector(
      np.cross(
        self.u_vector,
        np.subtract(vertex_m2, vertex_m0)
      ),
      u_vector_mag
    )

    self.v_vector = normalize_vector(
      np.cross(self.normal_vector, self.u_vector),
      u_vector_mag
    )

    self.segment_vectors = [
      self.u_vector,
      np.subtract(vertex_m2, vertex_m1),
      np.subtract(vertex_m0, vertex_m2),
    ]


  def uv_coordinates_to_face_coordinates(self, uv_coordinates: UV, distance_multipler=1):
    local_vector = np.add(
      np.multiply(uv_coordinates[0], self.u_vector),
      np.multiply(uv_coordinates[1], self.v_vector)
    )
    return np.multiply(np.add(self.origin_vector, local_vector), distance_multipler)

  # def uv_path_to_line(self, path: tuple[PuzzleNode, PuzzleNode]) -> tuple[list,list]:
  #   face_a = path[0].face
  #   face_b = path[1].face
  #   if( face_a != face_b ):
  #       return (
  #           [0,0,0],
  #           [0,0,0]
  #       )
  #   coordinates_a = path[0].uv_coordinates
  #   coordinates_b = path[1].uv_coordinates
  #   return (
  #       self.uv_coordinates_to_face_coordinates(coordinates_a),
  #       self.uv_coordinates_to_face_coordinates(coordinates_b),
  #   )

  # def uv_path_to_rectangle(self, path: tuple[PuzzleNode, PuzzleNode]):
  #   line = self.uv_path_to_line(path)
  #   line_vector = np.subtract(line[1], line[0])
  #   left_vector = normalize_vector(np.cross(line_vector, self.normal_vector), PUZZLE_PATH_WIDTH / 2)
  #   right_vector = normalize_vector(np.cross(self.normal_vector, line_vector), PUZZLE_PATH_WIDTH / 2)

  #   left_0 = np.add(line[0], left_vector)
  #   right_0 = np.add(line[0], right_vector)
  #   left_1 = np.add(line[1], left_vector)
  #   right_1 = np.add(line[1], right_vector)

  #   return [
  #     left_0, left_1, right_0, # rect bottom-left
  #     right_0, left_1, right_1, # rect top-right
  #   ]

  # def node_to_hexagon(self, node: PuzzleNode):
  #   hexagon_point_vertices = []
  #   point_coordinates = self.uv_coordinates_to_face_coordinates(node.uv_coordinates)
  #   hex_base = PUZZLE_PATH_WIDTH / 6
  #   skip_triangles = []
  #   half_triangles = []
  #   if node.is_edge:
  #     skip_triangles = [
  #       (6 + 2 * node.segment_idx) % 6,
  #       (1 + 2 * node.segment_idx) % 6,
  #     ]
  #     half_triangles = [
  #       (2 + 2 * node.segment_idx) % 6,
  #       (5 + 2 * node.segment_idx) % 6,
  #     ]
  #   last_leg = None
  #   for ix in range(-1,6):
  #     this_leg_uv = np.add(node.uv_coordinates, [
  #       hex_base * np.sin(ix * RAD60),
  #       -hex_base * np.cos(ix * RAD60)
  #     ])
  #     this_leg = self.uv_coordinates_to_face_coordinates(this_leg_uv)
  #     if last_leg is not None and ix not in skip_triangles:
  #       if len(half_triangles) > 0:
  #         if ix == half_triangles[0]:
  #           last_leg_uv = np.add(node.uv_coordinates, [
  #             hex_base * SIN60 * np.sin((ix-0.5) * RAD60),
  #             -hex_base * SIN60 * np.cos((ix-0.5) * RAD60)
  #           ])
  #           last_leg = self.uv_coordinates_to_face_coordinates(last_leg_uv)
  #         elif ix == half_triangles[1]:
  #           this_leg_uv = np.add(node.uv_coordinates, [
  #             hex_base * SIN60 * np.sin((ix-0.5) * RAD60),
  #             -hex_base * SIN60 * np.cos((ix-0.5) * RAD60)
  #           ])
  #           this_leg = self.uv_coordinates_to_face_coordinates(this_leg_uv)

  #       hexagon_point_vertices = hexagon_point_vertices + [
  #         point_coordinates, last_leg, this_leg
  #       ]
  #     last_leg = this_leg
  #   return hexagon_point_vertices


class Face(Renderable):

  def __init__(self,
    face_vertices: tuple[Vertex, Vertex, Vertex],
    puzzle_face: PuzzleFace,
    ctx: moderngl.Context,
    texture_location: int,
    vertex_uvs: tuple[UV, UV, UV],
    ):
    self.face_vertices = face_vertices

    self.coordinate_system = FaceCoordinateSystem(
      puzzle_face.generator_definition, *face_vertices
    )
    self.puzzle_face = puzzle_face

    self.path_vertices = self.__make_path_vertices()

    self.matrix = glm.mat4()

    self.face_shader = get_shader_program(ctx, "image")
    self.face_shader['u_texture_0'] = texture_location
    self.face_buffer = self.__make_vbo_with_uv(ctx, self.face_vertices, vertex_uvs)
    self.face_vertex_array = self.__make_vao(
      ctx,
      self.face_shader,
      [(self.face_buffer, "2f 3f", "in_textcoord_0", "in_position")]
    )

    self.path_shader = get_shader_program(ctx, "line")
    self.path_buffer = self.__make_vbo_with_color(ctx, self.path_vertices, INACTIVE_LINE_COLOR)
    self.path_vertex_array = self.__make_vao(
      ctx,
      self.path_shader,
      [(self.path_buffer, "3f 3f", "in_color", "in_position")]
    )

    self.nv = glm.vec3(self.coordinate_system.normal_vector)
    self.is_rotating = False
    self.current_angle = 0
    self.time_elapsed = 0

  def __make_path_vertices(self):
    polygons = self.puzzle_face.polygons
    path_vertices = []
    for polygon in polygons:
      path_line_vertices = [
        self.coordinate_system.uv_coordinates_to_face_coordinates(node.uv_coordinates) for node in polygon.nodes
      ]
      path_vertices = path_vertices + path_line_vertices
    return path_vertices

  def __make_vao(self, ctx, shader, context):
    return ctx.vertex_array(shader, context)

  def __make_vbo_with_color(self, ctx, vertices, color):
    zipped = [[*color, *v] for v in vertices]
    return ctx.buffer(np.array(zipped, dtype='f4'))

  def __make_vbo_with_uv(self, ctx, vertices, uvs):
    zipped = merge_collection_items(uvs, vertices)
    return ctx.buffer(np.array(zipped, dtype='f4'))


  def __rotate_by_degrees(self, degrees):
    self.matrix = glm.rotate(glm.mat4(), glm.radians(degrees), self.nv)

  # TODO replace linear function with ease-in
  def __animate_rotate(self):
    if self.time_elapsed > ROTATION_DURATION and self.current_angle < ROTATION_TARGET_ANGLE:
      self.__rotate_by_degrees(ROTATION_TARGET_ANGLE)
      self.is_rotating = False
    else:
      self.current_angle = ROTATION_TARGET_ANGLE * self.time_elapsed / ROTATION_DURATION
      if self.current_angle > ROTATION_TARGET_ANGLE:
        self.current_angle = ROTATION_TARGET_ANGLE
      self.__rotate_by_degrees(self.current_angle)
      if self.current_angle == ROTATION_TARGET_ANGLE:
        self.is_rotating = False

  def renderFace(self, camera: Camera, model_matrix, delta_time):
      m_mvp = camera.view_projection_matrix() * model_matrix * self.matrix
      self.face_shader["m_mvp"].write(m_mvp)
      self.face_vertex_array.render()
      self.path_shader["m_mvp"].write(m_mvp)
      self.path_vertex_array.render()

      if self.is_rotating:
        self.time_elapsed += delta_time
        self.__animate_rotate()


  def rotate(self):
    self.is_rotating = True
    self.current_angle = 0
    self.time_elapsed = 0
    self.puzzle_face.rotate()


  def destroy(self):
      self.face_buffer.release()
      self.path_buffer.release()
      self.face_shader.release()
      self.path_shader.release()
      self.face_vertex_array.release()
      self.path_vertex_array.release()

  def projected_vertices(self, matrix):
     return [glm.vec3(matrix * self.matrix * glm.vec4(v, 1.0)) for v in self.face_vertices]