

class PuzzlePolygon:
  def __init__(self, face, nodes: list):
    self.face = face
    self.nodes = set(nodes)
    self.neighbors = set()

  def is_closed(self, visited_nodes: set):
    #TODO: determine if the path inscribed by this polygon is closed
    # (Every path out of a node is also a path into it)
    pass
