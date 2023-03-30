import numpy as np

def triangle_vertices_from_indices(vertices, indices):
    triangle_vertices = [vertices[ind] for triangle in indices for ind in triangle]
    return np.array(triangle_vertices, dtype="f4")