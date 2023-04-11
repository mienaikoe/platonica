from enum import Enum
import math

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

# https://www.goldennumber.net/what-is-phi/
φ = (1 + math.sqrt(5)) / 2


def face_vertices_from_indices(
    vertices: list[tuple[float,float,float]],
    face_indices: list[tuple[int,int,int]]
):
    face_vertices = []
    for vert_indices in face_indices:
        face_vertices.append(
            [vertices[vert_index] for vert_index in vert_indices]
        )
    return face_vertices

SHAPE_VERTICES = {
  Shape.tetrahedron: face_vertices_from_indices([
    ( 1,  1,  1),
    (-1,  1, -1),
    ( 1, -1, -1),
    (-1, -1,  1)
  ], [
    (2, 3, 0),
    (3, 2, 1),
    (1, 0, 3),
    (0, 1, 2)
  ]),
  Shape.cube: face_vertices_from_indices([
    (-1, -1, 1),    # 0
    (1, -1, 1),     # 1
    (1, 1, 1),      # 2
    (-1, 1, 1),     # 3
    (-1, 1, -1),    # 4
    (-1, -1, -1),   # 5
    (1, -1, -1),    # 6
    (1, 1, -1),     # 7
  ],[
    (0, 3, 2, 1), # Z = 1
    (0, 5, 4, 3), # X = -1
    (3, 4, 7, 2), # Y = 1
    (2, 7, 6, 1), # X = 1
    (4, 5, 6, 7), # Z = -1
    (5, 0, 1, 6), # Y = -1
  ]),
  Shape.octahedron: face_vertices_from_indices([
    (1.0, 0.0, 0.0),
    (-1.0, 0.0, 0.0),
    (0.0, 1.0, 0.0),
    (0.0, -1.0, 0.0),
    (0.0, 0.0, 1.0),
    (0.0, 0.0, -1.0)
  ],[
    (2, 0, 4),
    (0, 2, 5),
    (1, 2, 4),
    (2, 1, 5),
    (3, 1, 4),
    (1, 3, 5),
    (0, 3, 4),
    (3, 0, 5)
  ]),
  Shape.icosahedron: face_vertices_from_indices([
    (0.8506507873535156, 0.525731086730957, 0.0),
    (-0.8506507873535156, 0.525731086730957, 0.0),
    (0.8506507873535156, -0.525731086730957, 0.0),
    (-0.8506507873535156, -0.525731086730957, 0.0),

    (0.525731086730957, 0.0, 0.8506507873535156),
    (0.525731086730957, 0.0, -0.8506507873535156),
    (-0.525731086730957, 0.0, 0.8506507873535156),
    (-0.525731086730957, 0.0, -0.8506507873535156),

    (0.0, 0.8506507873535156, 0.525731086730957),
    (0.0, -0.8506507873535156, 0.525731086730957),
    (0.0, 0.8506507873535156, -0.525731086730957),
    (0.0, -0.8506507873535156, -0.525731086730957),
  ], [
    (0, 4, 8),
    (4, 0, 2),
    (5, 2, 0),
    (2, 5, 11),

    (10, 0, 8),
    (0, 10, 5),
    (7, 5, 10),
    (5, 7, 11),

    (1, 10, 8),
    (10, 1, 7),
    (3, 7, 1),
    (7, 3, 11),

    (6, 1, 8),
    (1, 6, 3),
    (9, 3, 6),
    (3, 9, 11),

    (4, 6, 8),
    (6, 4, 9),
    (2, 9, 4),
    (9, 2, 11),
  ]),
  Shape.dodecahedron: face_vertices_from_indices([
    # https://en.wikipedia.org/wiki/Regular_dodecahedron#Cartesian_coordinates
    (-1, -1, 1),    # 0
    (1, -1, 1),     # 1
    (1, 1, 1),      # 2
    (-1, 1, 1),     # 3
    (-1, 1, -1),    # 4
    (-1, -1, -1),   # 5
    (1, -1, -1),    # 6
    (1, 1, -1),     # 7

    # blue
    (1/φ, 0, φ), # 8 1
    (1/φ, 0, -φ),
    (-1/φ, 0, φ), # 1
    (-1/φ, 0, -φ),

    # green
    (0, φ, 1/φ), # 12 1
    (0, φ, -1/φ),
    (0, -φ, 1/φ), # 1
    (0, -φ, -1/φ),

    # pink
    (φ, 1/φ, 0), # 16
    (φ, -1/φ, 0),
    (-φ, 1/φ, 0),
    (-φ, -1/φ, 0),
  ],[
    # clockwise, because our normals are inverted
    # top one facing me with two blues
    (10, 8, 1, 14, 0),
    # top, facing left
    (18, 3, 10, 0, 19),
    # mid back left
    (4, 13, 12, 3, 18),
    # mid back right
    (13, 7, 16, 2, 12),
    # top, facing right
    (2, 16, 17, 1, 8),
    # other top facing away
    (8, 10, 3, 12, 2),

     # bottom back
    (11, 9, 7, 13, 4),
    # bottom left
    (19, 5, 11, 4, 18),
    # mid front left
    (0, 14, 15, 5, 19),
    # mid front right
    (14, 1, 17, 6, 15),
     # bottom right
    (6, 17, 16, 7, 9),
    # bottom, front
    (9, 11, 5, 15, 6),
  ])
}
