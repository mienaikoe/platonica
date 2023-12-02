

class PuzzlePolygon:
  def __init__(self, face, nodes: list, is_active: bool):
    self.face = face
    self.nodes = nodes
    self.nodes_set = set(nodes)
    self.is_edge = len([node for node in self.nodes if node.is_edge]) >= 2
    self.neighbors = []
    self._active_neighbors = set()
    self.strange_face_neighbors = set()
    self.is_active = is_active
    self.key = "-".join([node.node_key for node in nodes])


  def associate(self, another_polygon: 'PuzzlePolygon'):
    if another_polygon.face != self.face:
      self.strange_face_neighbors.add(another_polygon)
      another_polygon.strange_face_neighbors.add(self)
    self._active_neighbors.add(another_polygon)
    another_polygon._active_neighbors.add(self)


  # def disassociate(self, another_polygon: 'PuzzlePolygon'):
  #   if another_polygon.face != self.face:
  #     self.strange_face_neighbors.remove(another_polygon)
  #     another_polygon.strange_face_neighbors.remove(self)
  #   self._active_neighbors.remove(another_polygon)
  #   another_polygon._active_neighbors.remove(self)


  def mates_with(self, another_polygon: 'PuzzlePolygon'):
    return len(self.nodes_set.intersection(another_polygon.nodes_set)) == 2


  def get_inactive_neighbor_lines(self):
    inactive_neighbor_lines = []
    for ix, this_node in enumerate(self.nodes):
      prev_node = self.nodes[
        len(self.nodes) - 1 if ix == 0 else ix - 1
      ]
      common_polygons = this_node.polygons.intersection(prev_node.polygons)
      for polygon in common_polygons:
        if polygon != self and not polygon.is_active:
          inactive_neighbor_lines.append((this_node, prev_node))
    return inactive_neighbor_lines


  def is_resonant(self, path_so_far: set['PuzzlePolygon']):
    if len(self._active_neighbors) < 2:
      return False

    path_so_far.add(self)
    next_neighbors = [
      neighbor for neighbor in self._active_neighbors if neighbor not in path_so_far
    ]
    for neighbor in next_neighbors:
      if neighbor in path_so_far:
        continue
      if not neighbor.is_resonant(path_so_far):
        return False
    path_so_far.remove(self)
    return True