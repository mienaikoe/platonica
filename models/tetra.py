import numpy as np

from models.model import Model
from models.helpers import triangle_vertices_from_indices
from engine.texture import texture_maps


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

class Tetrahedron(Model):

    def _get_vertex_data(self):
        return np.hstack([self.texture_vertices, tetrahedron_vertices])
