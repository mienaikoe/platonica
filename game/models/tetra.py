import numpy as np
from models.model import Model
from models.explode import ExplodingModel
from models.helpers import face_vertices_from_indices


vertex_palette = [(1, 1, 1), (-1, 1, -1), (1, -1, -1), (-1, -1, 1)]
face_vertices = [(2, 3, 0), (3, 2, 1), (1, 0, 3), (0, 1, 2)]


class Tetrahedron(Model):
    def __init__(self, ctx, camera, puzzle):
        vertices = face_vertices_from_indices(vertex_palette, face_vertices)
        super().__init__(ctx, camera, vertices, puzzle, "david-jorre-unsplash.png")


class PopTetra(ExplodingModel):
    def __init__(self, ctx, camera):
        vertices = face_vertices_from_indices(vertex_palette, face_vertices)
        super().__init__(ctx, camera, vertices)
