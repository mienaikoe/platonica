import glm
import numpy as np

def normalize_vector(vector: np.ndarray, target_magnitude: float):
    vector_magnitude = np.linalg.norm(vector)
    magnitude_ratio = (vector_magnitude / target_magnitude)
    return vector / magnitude_ratio

class UnitVector:
    UP = glm.vec3(0, 1, 0)
    RIGHT = glm.vec3(1, 0, 0)
    FORWARD = glm.vec3(0, 0, -1)

