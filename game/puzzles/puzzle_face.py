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
    self.polygons = []
    self.active_polygons = set()
    self.rotations = 0

    # Create all nodes
    for vertex in face_json['vertices']:
      indices = (vertex['indices'])
      node = PuzzleNode.from_node_json(self, vertex)
      self.nodes[indices[0]][indices[1]] = node

    # Create polygons between nodes
    for polygon in face_json['polygons']:
      polygon_indices = polygon['indices']
      polygon_nodes = [self.nodes[indices[0]][indices[1]] for indices in polygon_indices]

      polygon = PuzzlePolygon(self, polygon_nodes, polygon['is_active'])
      self.polygons.append(polygon)
      if polygon.is_active:
        self.active_polygons.add(polygon)
      for node in polygon_nodes:
        node.polygons.add(polygon)

    # Associate Active Polygons
    for polygon_a in list(self.active_polygons):
      for polygon_b in list(self.active_polygons):
        if polygon_a.key == '3,2,12-3,3,19-3,3,20':
          print("woo", polygon_a.key, polygon_b.key, polygon_a.mates_with(polygon_b))
        if polygon_a == polygon_b:
          continue
        if polygon_a.mates_with(polygon_b):
          polygon_a.associate(polygon_b)

  def edge_nodes_for_segment(self, segment_idx: int):
    self.generator_definition.vertex_range_for_segment(segment_idx, self.depth)

  def rotate(self, rotations: int):
    # new_strange_face_neighbors = {}
    # edge_polygons = [polygon for polygon in self.polygons if polygon.is_edge]
    # for polygon in edge_polygons:
    #   donor_nodes = []
    #   for node in polygon.nodes:
    #     if not node.is_edge:
    #       continue
    #     count_idx = self.generator_definition.rotated_count_idx(
    #       self.depth, node.indices[1], self.rotations + 1
    #     )
    #     donor_nodes.append(self.nodes[self.depth][count_idx])
    #   donor_polygons = donor_nodes[0].polygons.intersection(donor_nodes[1].polygons)
    #   donor_polygon = list(donor_polygons)[0]

    #   if donor_polygon.is_active:
    #     print(donor_polygon.key + "(active) donating to " + polygon.key)

    #   new_strange_face_neighbors[polygon.key] = donor_polygon.strange_face_neighbors

    # for polygon in edge_polygons:
    #   for sfn in list(polygon.strange_face_neighbors):
    #     polygon.disassociate(sfn)
    #   for sfn in new_strange_face_neighbors[polygon.key]:
    #     polygon.associate(sfn)
    self.rotations = rotations
