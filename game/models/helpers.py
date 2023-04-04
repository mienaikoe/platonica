import numpy as np
import json

def triangle_vertices_from_indices(
    vertices: list[tuple[float,float,float]],
    indices: list[tuple[int,int,int]]
):
    """
    @returns: an np.array with shape [len(indices), 3]
    representing the 3-vectors for all of the vertices of the shape
    """
    triangle_vertices = [vertices[ind] for triangle in indices for ind in triangle]
    return np.array(triangle_vertices, dtype="f4")

def face_vertices_from_indices(
    vertices: list[tuple[float,float,float]],
    indices: list[tuple[int,int,int]]
):
    face_vertices = []
    for i in indices:
        v0 = vertices[i[0]]
        v1 = vertices[i[1]]
        v2 = vertices[i[2]]
        face_vertices.append((v0, v1, v2))
    return face_vertices

def merge_collection_items(a: list, b: list):
    alen = len(a)
    if alen != len(b):
        raise Exception('length of both collections must be equal')
    i = 0
    c = []
    while i < alen:
        c.append([*a[i], *b[i]])
        i += 1
    return c