import numpy as np
import json
from models.model import Model
from models.helpers import triangle_vertices_from_indices, path_to_line



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

face_coordinates = []
for face in face_vertices:
    vertex_origin = vertex_palette[face[0]]
    vertex_x = vertex_palette[face[1]]
    right_vector = np.subtract(vertex_origin, vertex_x)
    right_unit_vector = 2 * right_vector / np.linalg.norm(right_vector)
    up_vector = np.cross(vertex_origin, right_vector)
    up_unit_vector = 2 * up_vector / np.linalg.norm(up_vector)
    face_coordinates.append((right_unit_vector, up_unit_vector))

class Tetrahedron(Model):

    def _get_puzzle_vertex_data(self):
        """
        returns a list of 6-arrays, representing the 3-vector
        beginnings and ends of each puzzle line.
        """
        paths = self.puzzle.collect_paths()

        line_coordinates = []
        for path in paths:
            if path[0].face != path[1].face:
                continue # we don't need to render ridge nodes
            face_idx = path[0].face.face_idx
            this_face_coordinates = face_coordinates[face_idx]
            vec_origin = vertex_palette[face_vertices[face_idx][0]]
            line = path_to_line(path, this_face_coordinates, vec_origin)
            line_coordinates.append(line[0])
            line_coordinates.append(line[1])

        # print(json.dumps(line_coordinates))

        return np.array(line_coordinates, dtype='f4')

    def _get_shape_vertex_data(self):
        """
        returns correlated data that can be used in shaders
        [
            (red, green, x, y, z)
        ]
        """
        ret = np.hstack([self.texture_vertices, tetrahedron_vertices])
        return ret
