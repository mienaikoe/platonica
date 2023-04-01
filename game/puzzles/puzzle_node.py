from __future__ import annotations
from enum import Enum

class PuzzleNodeType(Enum):
  start = 'start'
  hole = 'hole'

class PuzzleNode:

  @staticmethod
  def from_node_json(face, node_json: dict):
    return PuzzleNode(
      face,
      node_json['indices'],
      node_json['coordinates'],
      node_json['type'],
      []
    )

  def __init__(self,
    face: int,
    indices: tuple[int,int,int],
    coordinates: tuple[int,int,int],
    type: PuzzleNodeType,
    paths: list[PuzzleNode]
  ):
    self.face = face
    self.indices = indices
    self.coordinates = coordinates
    self.type = type
    self.paths = set(paths)
    self.is_active = False
    self.node_key = f"{chr(self.face.face_idx)},{','.join([chr(idx) for idx in self.indices])}"

  def can_reach_end(self, visited_nodes: set):
    if self.type == 'hole':
      return True
    for path in self.paths:
      if path in visited_nodes:
        continue
      visited_nodes.add(path)
      if path.travel_paths(visited_nodes):
        return True
    return False
