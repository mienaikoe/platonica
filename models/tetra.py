import moderngl
import numpy as np

from engine.camera import Camera
from models.model import Model
from models.helpers import triangle_vertices_from_indices
from engine.texture import get_texture, texture_maps


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

class Tetrahedron(Model):
    def __init__(self, ctx: moderngl.Context, camera: Camera):
        self.texture_file = 'tetra_tex_test.png'
        texture = get_texture(ctx, 'assets/textures/' + self.texture_file)
        super().__init__(ctx, camera, texture)

    def get_vertex_data(self):
        tex_map = texture_maps[self.texture_file]
        texture_vertices = triangle_vertices_from_indices(tex_map['uv'], tex_map['faces'])
        return np.hstack([texture_vertices, geom_vertices])