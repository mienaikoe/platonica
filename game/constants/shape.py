
from enum import Enum


class Shape(Enum):
  tetrahedron = "tetrahedron"
  cube = "cube"
  octahedron = "octahedron"
  dodecahedron = "dodecahedron"
  icosahedron = "icosahedron"

class FaceShape(Enum):
  triangle = 'triangle'
  square = 'square'
  pentagon = 'pentagon'
