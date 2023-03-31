import json
import os
from puzzles.face_coordinate_system import FaceCoordinateSystem

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
    self.coordinate_system = FaceCoordinateSystem.from_shape(self.shape)
    self.depth = puzzle_json['depth']

    faces = puzzle_json['faces']
    self.faces = []

    for (face_ix, face_definition) in enumerate(faces):
      face = PuzzleFace(self.shape, self.depth, face_ix, face_definition)
      self.faces.append(face)
      if face.start_node:
        self.start_face = face
        self.start_node = face.start_node

    self._associate_ridge_nodes(True)


  def _associate_ridge_nodes(self, connect: bool):
    for (edge_a, edge_b, same_direction) in ShapeFaceRidges[self.shape]:
      ring_a = self.faces[edge_a[0]].nodes[self.depth]
      ring_b = self.faces[edge_b[0]].nodes[self.depth]
      vertex_range_a = self.coordinate_system.vertex_range_for_segment(edge_a[1], self.depth)
      vertex_range_b = self.coordinate_system.vertex_range_for_segment(edge_b[1], self.depth)
      nodes_a = [ring_a[ix] for ix in vertex_range_a]
      nodes_b = [ring_b[ix] for ix in vertex_range_b]
      vertex_count = len(nodes_a)

      for ix in range(vertex_count):
        node_a = nodes_a[ix]
        node_b = nodes_b[ix] if same_direction else nodes_b[vertex_count-ix-1]

        if not node_a or not node_b:
          # nodes are only available if they have paths
          continue
        if connect:
          node_a.paths.add(node_b)
          node_b.paths.add(node_a)
        else:
          if node_b in node_a.paths:
            node_a.paths.remove(node_b)
          if node_a in node_b.paths:
            node_b.paths.remove(node_a)







