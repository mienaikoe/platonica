import json
import os
from puzzles.face_generator_definition import FaceGeneratorDefinition

from puzzles.puzzle_face import PuzzleFace

dir_path = os.path.dirname(os.path.realpath(__file__))

from constants.shape import Shape
from puzzles.shape_face_ridges import ShapeFaceRidges

def get_puzzle_file(puzzle_file_name: str):
  with open(os.path.join(dir_path, 'generated', f'{puzzle_file_name}.json'), 'r') as fp:
    puzzle_json_str = fp.read()
    return json.loads(puzzle_json_str)


class PuzzleGraph():
  @staticmethod
  def from_file_name(puzzle_file_name: str):
    puzzle_json = get_puzzle_file(puzzle_file_name)
    return PuzzleGraph(puzzle_json)

  def __init__(self, puzzle_json: dict):
    self.shape = Shape[puzzle_json['shape']]
    self.coordinate_system = FaceGeneratorDefinition.from_shape(self.shape)
    self.depth = puzzle_json['depth']

    faces = puzzle_json['faces']
    self.faces = []

    for (face_idx, face_definition) in enumerate(faces):
      face = PuzzleFace(self.shape, self.depth, face_idx, face_definition)
      self.faces.append(face)

  #   self._associate_ridge_polygons()

  # def _associate_ridge_polygons(self):
  #   for (edge_a, edge_b, same_direction) in ShapeFaceRidges[self.shape]:
  #     last_idx = self.coordinate_system.vertex_count_for_ring(self.depth) - 1
  #     ring_a = self.faces[edge_a[0]].nodes[self.depth]
  #     ring_b = self.faces[edge_b[0]].nodes[self.depth]
  #     vertex_range_a = self.coordinate_system.vertex_range_for_segment(edge_a[1], self.depth, extra=1)
  #     vertex_range_b = self.coordinate_system.vertex_range_for_segment(edge_b[1], self.depth, extra=1)
  #     nodes_a = [ring_a[ix if ix <= last_idx else 0] for ix in vertex_range_a]
  #     nodes_b = [ring_b[ix if ix <= last_idx else 0] for ix in vertex_range_b]
  #     vertex_count = len(nodes_a)

  #     node_pair = (None, None)
  #     node_pair_prev = (None, None)

  #     for ix in range(vertex_count):
  #       node_pair_prev = node_pair
  #       node_pair = [
  #         nodes_a[ix],
  #         nodes_b[ix] if same_direction else nodes_b[(vertex_count-1)-ix]
  #       ]

  #       if not node_pair_prev[0] or not node_pair_prev[1] or not node_pair[0] or not node_pair[1]:
  #         continue

  #       polygons_pair = [
  #         node_pair[0].polygons.intersection(node_pair_prev[0].polygons),
  #         node_pair[1].polygons.intersection(node_pair_prev[1].polygons),
  #       ]
  #       if len(polygons_pair[0]) != 1 or len(polygons_pair[1]) != 1:
  #         continue
  #       polygon_a = polygons_pair[0].pop()
  #       polygon_b = polygons_pair[1].pop()

  #       if not polygon_a.is_edge or not polygon_b.is_edge:
  #         continue
  #       if not polygon_b.is_active or not polygon_b.is_active:
  #         continue
  #       polygon_a.associate(polygon_b) # method automatically bidirectionally associates


  def collect_polygons(self):
    return [polygon for face in self.faces for polygon in face.polygons]

  def is_resonant(self):
    # print("=== Resonance ===")
    # start_polygon = list(self.faces[0].active_polygons)[0]
    # return start_polygon.is_resonant(set())
    for face in self.faces:
      if face.rotations != 0:
        return False
    return True








