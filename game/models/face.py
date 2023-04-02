import json
import numpy as np
import glm
import moderngl

from constants.colors import Colors
from engine.renderable import Renderable
from engine.camera import Camera
from engine.shader import get_shader_program
from puzzles.puzzle_node import PuzzleNode
from puzzles.puzzle_face import PuzzleFace
from models.types import Vertex

LINE_COLOR = Colors.WHITE
DEFAULT_FACE_COLOR = Colors.GRAY
ACTIVE_FACE_COLOR = Colors.GREEN

test_colors = [
   (0.0, 0.0, 0.5),
   (0.5, 0.0, 0.0),
   (0.0, 0.5, 0.0),
   (0.5, 0.4, 0.0),
]

def normalize_vector(vector: tuple[float, float, float], target_magnitude: float):
    vector_magnitude = np.linalg.norm(vector)
    magnitude_ratio = (vector_magnitude / target_magnitude)
    return vector / magnitude_ratio

DISTANCE_MULTIPLER = 1.1
# This helps us render the lines above the face instead of inside it

class FaceCoordinateSystem:

  def __init__(self, vertex_0, vertex_1, vertex_2):
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


  def uv_coordinates_to_face_coordinates(self, uv_coordinates: tuple[float, float]):
    local_vector = np.add(
      np.multiply(uv_coordinates[0], self.u_vector),
      np.multiply(uv_coordinates[1], self.v_vector)
    )

    return np.add(self.origin_vector, local_vector)

  def uv_path_to_line(self, path: tuple[PuzzleNode, PuzzleNode]) -> tuple[list,list]:
    face_a = path[0].face
    face_b = path[1].face
    if( face_a != face_b ):
        return (
            [0,0,0],
            [0,0,0]
        )
    coordinates_a = path[0].coordinates
    coordinates_b = path[1].coordinates
    return (
        self.uv_coordinates_to_face_coordinates(coordinates_a),
        self.uv_coordinates_to_face_coordinates(coordinates_b),
    )

class Face(Renderable):

  def __init__(self,
    face_vertices: tuple[Vertex, Vertex, Vertex],
    puzzle_face: PuzzleFace,
    ctx: moderngl.Context,
    ):
    self.face_vertices = face_vertices

    self.coordinate_system = FaceCoordinateSystem(*face_vertices)
    self.puzzle_face = puzzle_face
    paths = puzzle_face.collect_paths()
    path_vertices = []
    for path in paths:
      if path[0].face != path[1].face:
          continue # we don't need to render ridge nodes
      line = self.coordinate_system.uv_path_to_line(path)
      path_vertices.append(line[0])
      path_vertices.append(line[1])
    self.path_vertices = path_vertices

    self.matrix = glm.mat4()

    self.face_shader = get_shader_program(ctx, "default")
    self.face_buffer = self.__make_vbo(ctx, self.face_vertices, test_colors[puzzle_face.face_idx])
    self.face_vertex_array = self.__make_vao(ctx, self.face_shader, self.face_buffer)

    self.path_shader = get_shader_program(ctx, "line")
    self.path_buffer = self.__make_vbo(ctx, self.path_vertices, LINE_COLOR)
    self.path_vertex_array = self.__make_vao(ctx, self.path_shader, self.path_buffer)

  def __make_vao(self, ctx, shader, buffer):
    return ctx.vertex_array(shader, [(buffer, "3f 3f", "in_color", "in_position")])

  def __make_vbo(self, ctx, vertices, color):
    zipped = [[*color, *v] for v in vertices]
    return ctx.buffer(np.array(zipped, dtype='f4'))

  def renderFace(self, camera: Camera, model_matrix):
      m_mvp = camera.projection_matrix * camera.view_matrix * model_matrix * self.matrix
      self.face_shader["m_mvp"].write(m_mvp)
      self.face_vertex_array.render()
      self.path_shader["m_mvp"].write(m_mvp)
      self.path_vertex_array.render(moderngl.LINES)
  
  def rotate(self):
    nv = glm.vec3(self.coordinate.normal_vector)
    self.matrix = glm.rotate(self.matrix, glm.radians(120), nv)
    self.puzzle_face.rotate()

  def destroy(self):
      self.face_buffer.release()
      self.path_buffer.release()
      self.face_shader.release()
      self.path_shader.release()
      self.face_vertex_array.release()
      self.path_vertex_array.release()
