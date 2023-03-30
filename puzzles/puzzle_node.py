from __future__ import annotations
from enum import Enum
import glm

class PuzzleNodeType(Enum):
  start = 'start'
  hole = 'hole'

class PuzzleNode:
  @staticmethod
  def merge(puzzle_node_a: PuzzleNode, puzzle_node_b: PuzzleNode):
    return PuzzleNode(
      indices=None,
      coordinates=puzzle_node_a.coordinates,
      type=None,
      paths=puzzle_node_a.paths + puzzle_node_b.paths
    )

  @staticmethod
  def from_node_json(transformation_matrix: glm.mat4, node_json: dict):
    # TODO: Get transformation matrix from face_key
    flat_coordinates = node_json['coordinates']
    glm_coordinates = glm.vec3()
    return PuzzleNode(node_json['indices'], glm_coordinates, node_json['type'], [])

  def __init__(self, indices: tuple[int,int,int], coordinates: glm.vec3, type: PuzzleNodeType, paths: list[PuzzleNode]):
    self.indices = indices
    self.coordinates = coordinates
    self.type = type
    self.paths = paths

  def add_path(self, node):
    self.paths.append(node)