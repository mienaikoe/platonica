import numpy as np
import json
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

def uv_to_face_coordinates(
    face_coordinates: tuple[tuple[float,float,float],tuple[float,float,float]],
    vec_origin: tuple[float, float, float],
    uv_coordinates: tuple[float, float]
):
    ret = np.add(
        np.add(vec_origin, np.multiply(uv_coordinates[0], face_coordinates[0])),
        np.add(vec_origin, np.multiply(uv_coordinates[1], face_coordinates[1])),
    ).tolist()

    print(face_coordinates, uv_coordinates, json.dumps(ret))

    return ret


def path_to_line(
    path: tuple[PuzzleNode, PuzzleNode],
    face_coordinates: tuple[float,float],
    vec_origin: tuple[float,float,float]
):
    face_a = path[0].face
    face_b = path[1].face
    if( face_a != face_b ):
        return np.array((0,0,0,0,0,0), dtype="f4")
    coordinates_a = path[0].coordinates
    coordinates_b = path[1].coordinates
    return (
        uv_to_face_coordinates(face_coordinates, vec_origin, coordinates_a),
        uv_to_face_coordinates(face_coordinates, vec_origin, coordinates_b),
    )
