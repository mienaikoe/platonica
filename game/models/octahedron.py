import numpy as np
from constants.colors import Colors
from models.model import Model
from models.helpers import face_vertices_from_indices

vertex_palette = [
    (1.0, 0.0, 0.0),
    (-1.0, 0.0, 0.0),
    (0.0, 1.0, 0.0),
    (0.0, -1.0, 0.0),
    (0.0, 0.0, 1.0),
    (0.0, 0.0, -1.0)
]

face_vertices = [
    (4, 0, 2),
    (4, 2, 1),
    (4, 1, 3),
    (4, 3, 0),
    (5, 2, 0),
    (5, 1, 2),
    (5, 3, 1),
    (5, 0, 3)
]

class Octahedron(Model):

    def __init__(self, ctx, camera, puzzle):
        vertices = face_vertices_from_indices(vertex_palette, face_vertices)
        super().__init__(ctx, camera, vertices, puzzle, "generic.png")