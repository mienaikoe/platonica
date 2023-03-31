import glm
from constants.shape import Shape

"""
A list of tuples of tuples ((face, segment), (face, segment), same_direction).
Each face's segment of the outer ring corresponds with
another face's segment of its outer ring.
"""
ShapeFaceRidges: dict[Shape, list[tuple[tuple[int,int], tuple[int,int], bool]]] = {
  # 2 is the inside triangle
  Shape.tetrahedron: [
    # A
    ((0, 0), (1, 0), False),  # A & B
    ((0, 1), (2, 1), False),  # A & C
    ((0, 2), (3, 2), False),   # A & D
    ((1, 2), (2, 2), False),  # B & C
    ((1, 1), (3, 1), False),  # B & D
    ((2, 0), (3, 0), False),  # C & D
  ]
}
