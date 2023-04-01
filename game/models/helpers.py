import numpy as np
import json
from models.face_coordinate_system import FaceCoordinateSystem
from puzzles.puzzle_node import PuzzleNode

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


def face_coordinates_from_indices(
    vertices: list[tuple[float,float,float]],
    indices: list[tuple[int,int,int]]
):
    face_coordinates: list[FaceCoordinateSystem] = []
    for vert_index in indices:
        face_coordinates.append(
            FaceCoordinateSystem(
                vertices[vert_index[0]],
                vertices[vert_index[1]],
                vertices[vert_index[2]]
            )
        )
    return face_coordinates