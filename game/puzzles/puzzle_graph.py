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

    self._associate_ridge_polygons(True)

  def _associate_polygons(self, polygon_a, polygon_b, connect: bool):
    if connect:
      polygon_a.associate(polygon_b)
      polygon_b.neighbors.add(polygon_a)
    else:
      if polygon_b in polygon_a.neighbors:
        polygon_a.neighbors.remove(polygon_b)
      if polygon_a in polygon_b.paths:
        polygon_b.paths.remove(polygon_a)

  def _associate_ridge_polygons(self, connect: bool):
    for (edge_a, edge_b, same_direction) in ShapeFaceRidges[self.shape]:
      ring_a = self.faces[edge_a[0]].nodes[self.depth]
      ring_b = self.faces[edge_b[0]].nodes[self.depth]
      vertex_range_a = self.coordinate_system.vertex_range_for_segment(edge_a[1], self.depth)
      vertex_range_b = self.coordinate_system.vertex_range_for_segment(edge_b[1], self.depth)
      nodes_a = [ring_a[ix] for ix in vertex_range_a]
      nodes_b = [ring_b[ix] for ix in vertex_range_b]
      vertex_count = len(nodes_a)

      node_a_prev = None
      node_b_prev = None

      for ix in range(vertex_count):
        node_a = nodes_a[ix]
        node_b = nodes_b[ix] if same_direction else nodes_b[(vertex_count-1)-ix]

        if not node_a or not node_b:
          # nodes are only available if they have polygons into them
          continue

        if node_a_prev and node_b_prev:
          polygons_a = node_a.polygons.intersection(node_a_prev.polygons)
          polygons_b = node_b.polygons.intersection(node_b_prev.polygons)
          if len(polygons_a) > 0 and len(polygons_b) > 0:
            self._associate_polygons(polygons_a[0], polygons_b[0])

  def collect_polygons(self):
    return [polygon for face in self.faces for polygon in face.polygons]








