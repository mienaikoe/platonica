import numpy as np

from models.model import Model
from models.helpers import triangle_vertices_from_indices


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
tetrahedron_vertices = triangle_vertices_from_indices(vertex_palette, face_vertices)


color_palette = [
    (0.5, 0.2), # orange
    (0.0, 1.0), # green
    (1.0, 1.0), # yellow
]
face_colors = [
    (0, 1, 2), # orange on the first vertex, then green, then yellow
    (0, 1, 2),
    (0, 1, 2),
    (0, 1, 2),
]
color_texture_vertices = triangle_vertices_from_indices(color_palette, face_colors)

class Tetrahedron(Model):

    def _get_vertex_data(self):
        return np.hstack([color_texture_vertices, tetrahedron_vertices])