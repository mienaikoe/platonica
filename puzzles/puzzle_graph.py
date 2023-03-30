import json
import os

from puzzles.puzzle_face import PuzzleFace

dir_path = os.path.dirname(os.path.realpath(__file__))

from constants.shape import Shape
from puzzles.shape_transform_matrices import ShapeFaceRidges

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
    self.depth = puzzle_json['depth']

    faces = puzzle_json['faces']
    self.faces = []

    for (face_ix, face_definition) in enumerate(faces):
      face = PuzzleFace(self.depth, face_ix, face_definition)
      self.faces.append(face)
      if face.start_node:
        self.start_face = face
        self.start_node = face.start_node

    self._associate_ridge_nodes(True)


  def _associate_ridge_nodes(self, connect: bool):
    for vertexPairs in ShapeFaceRidges[self.shape]:
      vertex_a = vertexPairs[0]
      vertex_b = vertexPairs[1]
      node_a = self.faces[vertex_a[0]].nodes[vertex_a[1]][vertex_a[2]]
      node_b = self.faces[vertex_b[0]].nodes[vertex_b[1]][vertex_b[2]]
      if not node_a or not node_b:
        continue
      if connect:
        node_a.paths.add(node_b)
        node_b.paths.add(node_a)
      else:
        if node_b in node_a.paths:
          node_a.paths.remove(node_b)
        if node_a in node_b.paths:
          node_b.paths.remove(node_a)








