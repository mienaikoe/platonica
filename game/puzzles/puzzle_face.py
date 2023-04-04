from constants.shape import Shape
from puzzles.puzzle_polygon import PuzzlePolygon
from puzzles.face_generator_definition import FaceGeneratorDefinition
from puzzles.puzzle_node import PuzzleNode


class PuzzleFace:
  def __init__(self, shape: Shape, depth: int, face_idx: int, face_json: dict):
    self.depth = depth
    self.face_idx = face_idx
    self.generator_definition = FaceGeneratorDefinition.from_shape(shape)
    self.nodes = [[None] * (self.generator_definition.vertex_count_for_ring(ringIx)) for ringIx in range(depth+1)]
    self.polygons = set()

    # Create all nodes
    for vertex in face_json['vertices']:
      indices = (vertex['indices'])
      node = PuzzleNode.from_node_json(self, vertex)
      self.nodes[indices[0]][indices[1]] = node

    # Create polygons between nodes
    for polygon in face_json['polygons']:
      polygon_indices = polygon['indices']
      polygon_nodes = [self.nodes[indices[0]][indices[1]] for indices in polygon_indices]
      polygon = PuzzlePolygon(self, polygon_nodes)
      self.polygons.add(polygon)
      for node in polygon_nodes:
        node.polygons.add(polygon)

  def edge_nodes_for_segment(self, segment_idx: int):
    self.generator_definition.vertex_range_for_segment(segment_idx, self.depth)

  def rotate(self):
    # TODO
    pass