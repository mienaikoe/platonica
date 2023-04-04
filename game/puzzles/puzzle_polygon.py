

class PuzzlePolygon:
  def __init__(self, face, nodes: list, is_active: bool):
    self.face = face
    self.nodes = nodes
    self.nodes_set = set(nodes)
    self._neighbors = set()
    self._strange_face_neighbors = set()
    self.is_active = is_active

  def is_closed(self, visited_nodes: set):
    #TODO: determine if the path inscribed by this polygon is closed
    # (Every path out of a node is also a path into it)
    pass

  def associate(self, another_polygon: 'PuzzlePolygon'):
    if another_polygon.face != self.face:
      self._strange_face_neighbors.add(another_polygon)
      another_polygon._strange_face_neighbors.add(self)
    else:
      self._neighbors.add(another_polygon)
      another_polygon._neighbors.add(self)

  def mates_with(self, another_polygon: 'PuzzlePolygon'):
    return len(self.nodes_set.intersection(another_polygon.nodes_set)) == 2

  def get_neighbors(self):
    return self._neighbors + self._strange_face_neighbors

  def on_rotate(self):
    self._strange_face_neighbors.clear()