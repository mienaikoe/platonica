from models.model import Model
import numpy as np
from models.helpers import face_vertices_from_indices
cube_corners = [
    (-1, -1, 1),    # 0
    (1, -1, 1),     # 1
    (1, 1, 1),      # 2
    (-1, 1, 1),     # 3
    (-1, 1, -1),    # 4
    (-1, -1, -1),   # 5
    (1, -1, -1),    # 6
    (1, 1, -1),     # 7
]
cube_indices = [
    (0, 2, 3),
    (0, 1, 2),
    (1, 7, 2),
    (1, 6, 7),
    (6, 5, 4),
    (4, 7, 6),
    (3, 4, 5),
    (3, 5, 0),
    (3, 7, 4),
    (3, 2, 7),
    (0, 6, 1),
    (0, 5, 6),
]

class Cube(Model):
    def __init__(self, ctx, camera, puzzle):
        vertices = face_vertices_from_indices(cube_corners, cube_corners)
        super().__init__(ctx, camera, vertices, puzzle, "david-jorre-unsplash.png")
