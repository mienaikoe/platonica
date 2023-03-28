from models.model import Model
import numpy as np
from models.helpers import triangle_vertices_from_indices


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

texture_corners = [(1, 0), (1, 0), (1, 1)]
texture_indices = [
    (0, 1, 2),
    (2, 0, 1),
    (1, 2, 0),
    (0, 2, 1)
]
texture_vertices = triangle_vertices_from_indices(texture_corners, texture_indices)

class Tetrahedron(Model):
    def get_vertex_data(self):
        return np.hstack([texture_vertices, geom_vertices])
