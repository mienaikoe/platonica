from __future__ import annotations
from enum import Enum

class PuzzleNode:

  @staticmethod
  def from_node_json(face, node_json: dict):
    return PuzzleNode(
      face,
      node_json['indices'],
      node_json['coordinates']
    )

  def __init__(
    self,
    face: int,
    indices: tuple[int,int],
    uv_coordinates: tuple[int,int],
  ):
    self.face = face
    self.indices = indices
    self.uv_coordinates = uv_coordinates
    self.polygons = set()
    self.is_edge = indices[0] == face.depth
    self.segment_idx = face.generator_definition.segment_for_vertex(indices[0], indices[1])
    self.node_key = f"{chr(self.face.face_idx)},{','.join([chr(idx) for idx in self.indices])}"

