import json
import numpy
import glm
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

from constants.shape import Shape
from puzzles.puzzle_node import PuzzleNode
from puzzles.shape_transform_matrices import ShapeFaceRidges

def get_puzzle_file(puzzle_file_name: str):
  with open(os.path.join(dir_path, 'generated', f'{puzzle_file_name}.json'), 'r') as fp:
    puzzle_json_str = fp.read()
    return json.loads(puzzle_json_str)


class Puzzle:
  @staticmethod
  def from_file_name(puzzle_file_name: str):
    puzzle_json = get_puzzle_file(puzzle_file_name)
    return Puzzle(puzzle_json)

  def __init__(self, puzzle_json: dict):
    self.shape = Shape[puzzle_json['shape']]
    self.depth = puzzle_json['depth']

    faces = puzzle_json['faces']
    self.nodes = [
      [
        [None] * self.depth
      ] * self.depth
    ] * len(faces)

    for (face_ix, face_definition) in enumerate(faces):
      face_nodes = self.nodes[face_ix]

      # Create all nodes
      for vertex in face_definition['vertices']:
        indices = (vertex['indices'])
        # TODO: Get transformation matrix for face
        node = PuzzleNode.from_node_json(glm.mat4(), vertex)
        face_nodes[indices[0]][indices[1]] = node
        if node.type == 'start':
          self.start = node

      # Create paths between nodes
      for path in face_definition['paths']:
        from_indices = path[0]
        from_node = face_nodes[from_indices[0]][from_indices[1]]
        to_indices = path[1]
        to_node = face_nodes[to_indices[0]][to_indices[1]]
        from_node.add_path(to_node)
        to_node.add_path(from_node)

  def merge_ridge_nodes(self):
    # Merge edge nodes between faces
    for vertexPairs in ShapeFaceRidges[self.shape]:
      vertex_a = vertexPairs[0]
      vertex_b = vertexPairs[1]
      node_a = self.nodes[vertex_a[0]][vertex_a[1]][vertex_a[2]]
      node_b = self.nodes[vertex_b[0]][vertex_b[1]][vertex_b[2]]
      if not node_a or not node_b:
        continue
      merge_node = PuzzleNode.merge(node_a, node_b)
      for node in (node_a, node_b):
        for path_node in node.paths:
          path_node.paths.remove(node)
          path_node.paths.append(merge_node)








