import numpy as np
from models.model import Model
from models.explode import ExplodingModel
from models.helpers import face_vertices_from_indices

vertex_palette = [
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
]

face_vertices = [
    (0, 4, 8),  # LOCK
    (4, 0, 2),
    (5, 2, 0),
    (2, 5, 11),
    (10, 0, 8),  # LOCK
    (0, 10, 5),
    (7, 5, 10),
    (5, 7, 11),
    (1, 10, 8),  # LOCK
    (10, 1, 7),
    (3, 7, 1),
    (7, 3, 11),
    (6, 1, 8),  # LOCK
    (1, 6, 3),
    (9, 3, 6),
    (3, 9, 11),
    (4, 6, 8),  # LOCK
    (6, 4, 9),
    (2, 9, 4),
    (9, 2, 11),
]


class Icosahedron(Model):
    def __init__(self, ctx, camera, puzzle):
        vertices = face_vertices_from_indices(vertex_palette, face_vertices)
        super().__init__(ctx, camera, vertices, puzzle, "generic.png")


class PopIcosa(ExplodingModel):
    def __init__(self, ctx, camera):
        vertices = face_vertices_from_indices(vertex_palette, face_vertices)
        super().__init__(ctx, camera, vertices)
