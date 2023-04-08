import json
from models.model import Model
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
    (0, 3, 2, 1), # Z = 1
    (0, 5, 4, 3), # X = -1
    (3, 4, 7, 2), # Y = 1
    (2, 7, 6, 1), # X = 1
    (4, 5, 6, 7), # Z = -1
    (5, 0, 1, 6), # Y = -1
]

class Cube(Model):
    def __init__(self, ctx, camera, puzzle):
        vertices = face_vertices_from_indices(cube_corners, cube_indices)
        super().__init__(ctx, camera, vertices, puzzle, "david-jorre-unsplash.png")
