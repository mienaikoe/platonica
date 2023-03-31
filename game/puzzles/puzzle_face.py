from constants.shape import Shape
from puzzles.face_coordinate_system import FaceCoordinateSystem
from puzzles.puzzle_node import PuzzleNode


class PuzzleFace:
  def __init__(self, shape: Shape, depth: int, face_ix: int, face_json: dict):
    self.depth = depth
    self.face_ix = face_ix
    self.coordinate_system = FaceCoordinateSystem.from_shape(shape)
    self.nodes = [[None] * (self.coordinate_system.vertex_count_for_ring(ringIx)) for ringIx in range(depth+1)]
    self.start_node = None

    # Create all nodes
    for vertex in face_json['vertices']:
      indices = (vertex['indices'])
      # TODO: Get transformation matrix for face
      node = PuzzleNode.from_node_json(self, vertex)
      self.nodes[indices[0]][indices[1]] = node
      if node.type == 'start':
        self.start_node = node

    # Create paths between nodes
    for path in face_json['paths']:
      from_indices = path[0]
      from_node = self.nodes[from_indices[0]][from_indices[1]]
      to_indices = path[1]
      to_node = self.nodes[to_indices[0]][to_indices[1]]
      from_node.paths.add(to_node)
      to_node.paths.add(from_node)

  def edge_nodes_for_segment(self, segment_idx: int):
    self.coordinate_system.vertex_range_for_segment(segment_idx, self.depth)

  def rotate(self):
    # TODO
    pass