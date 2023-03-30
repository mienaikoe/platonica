import numpy as np

from models.model import Model

MOCK_VERTEX_ARRAY = [(-0.6, -0.8, 0.0), (0.6, -0.8, 0.0), (-0.0, 0.8, 0.0)]


class Triangle(Model):
    def _get_vertex_data(self):
        return np.array(MOCK_VERTEX_ARRAY, dtype="f4")
