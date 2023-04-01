import json
import numpy as np
from puzzles.puzzle_node import PuzzleNode


def normalize_vector(vector: tuple[float, float, float], target_magnitude: float):
    vector_magnitude = np.linalg.norm(vector)
    magnitude_ratio = (vector_magnitude / target_magnitude)
    return vector / magnitude_ratio

DISTANCE_MULTIPLER = 1.1
# This helps us render the lines above the face instead of inside it

class FaceCoordinateSystem:

  def __init__(self, vertex_0, vertex_1, vertex_2):
    vertex_m0 = np.multiply(vertex_0, DISTANCE_MULTIPLER)
    vertex_m1 = np.multiply(vertex_1, DISTANCE_MULTIPLER)
    vertex_m2 = np.multiply(vertex_2, DISTANCE_MULTIPLER)

    self.origin_vector = vertex_m0

    self.u_vector = np.subtract(vertex_m1, vertex_m0)
    u_vector_mag = np.linalg.norm(self.u_vector)

    self.normal_vector = normalize_vector(
      np.cross(
        self.u_vector,
        np.subtract(vertex_m2, vertex_m0)
      ),
      u_vector_mag
    )

    self.v_vector = normalize_vector(
      np.cross(self.normal_vector, self.u_vector),
      u_vector_mag
    )


  def uv_coordinates_to_face_coordinates(self, uv_coordinates: tuple[float, float]):
    local_vector = np.add(
      np.multiply(uv_coordinates[0], self.u_vector),
      np.multiply(uv_coordinates[1], self.v_vector)
    )

    return np.add(self.origin_vector, local_vector)

  def uv_path_to_line(self, path: tuple[PuzzleNode, PuzzleNode]) -> tuple[list,list]:
    face_a = path[0].face
    face_b = path[1].face
    if( face_a != face_b ):
        return (
            [0,0,0],
            [0,0,0]
        )
    coordinates_a = path[0].coordinates
    coordinates_b = path[1].coordinates
    return (
        self.uv_coordinates_to_face_coordinates(coordinates_a),
        self.uv_coordinates_to_face_coordinates(coordinates_b),
    )
