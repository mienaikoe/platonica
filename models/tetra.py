import moderngl
import numpy as np

from engine.camera import Camera
from models.model import Model
from models.helpers import triangle_vertices_from_indices
from engine.texture import get_texture


corners = [
    (1,1,1),
    (-1,1,-1),
    (1,-1,-1),
    (-1,-1,1)
]

face_indices = [
    (1, 2, 3),
    (0, 3, 2),
    (0, 1, 3),
    (0, 2, 1)
]

geom_vertices = triangle_vertices_from_indices(corners, face_indices)


texture_corners = [
    (0.5, 0.2), # orange
    (0.0, 1.0), # green
    (1.0, 1.0), # yellow
]
texture_indices = [
    (0, 1, 2),
    (0, 1, 2),
    (0, 1, 2),
    (0, 1, 2),
]
texture_vertices = triangle_vertices_from_indices(texture_corners, texture_indices)

class Tetrahedron(Model):
    def __init__(self, ctx: moderngl.Context, camera: Camera):
        texture = get_texture(ctx, 'assets/textures/texture_test.png')
        super().__init__(ctx, camera, texture)

    def get_vertex_data(self):
        return np.hstack([texture_vertices, geom_vertices])