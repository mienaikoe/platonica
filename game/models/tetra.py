import numpy as np
from constants.colors import Colors
from models.model import Model
from models.helpers import face_vertices_from_indices


vertex_palette = [
    (1,1,1),
    (-1,1,-1),
    (1,-1,-1),
    (-1,-1,1)
]
face_vertices = [
    (1, 2, 3),
    (0, 3, 2),
    (0, 1, 3),
    (0, 2, 1)
]

class Tetrahedron(Model):

    def __init__(self, ctx, camera, puzzle):
        vertices = face_vertices_from_indices(vertex_palette, face_vertices)
        super().__init__(ctx, camera, vertices, puzzle, "david-jorre-unsplash.png")
