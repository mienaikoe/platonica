import numpy as np
from models.model import Model
from models.helpers import triangle_vertices_from_indices, face_coordinates_from_indices


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

face_coordinates = face_coordinates_from_indices(vertex_palette, face_vertices)


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
            line = this_face_coordinates.uv_path_to_line(path)
            line_coordinates.append([0.5, 0.5, *(line[0])])
            line_coordinates.append([0.5, 0.5, *(line[1])])

        # print(json.dumps(line_coordinates, cls=NpEncoder))

        # for face in face_vertices:
        #     line_coordinates.append([0.0, 1.0, *vertex_palette[face[0]]])
        #     line_coordinates.append([0.0, 1.0, *vertex_palette[face[1]]])
        #     line_coordinates.append([0.0, 1.0, *vertex_palette[face[1]]])
        #     line_coordinates.append([0.0, 1.0, *vertex_palette[face[2]]])
        #     line_coordinates.append([0.0, 1.0, *vertex_palette[face[0]]])
        #     line_coordinates.append([0.0, 1.0, *vertex_palette[face[2]]])
                # UV
                # vertex_0 = vertex_palette[face[0]]
                # line_coordinates.append([1.0, ix / 3, 0,0,0])
                # line_coordinates.append([1.0, ix / 3, *right_line])
                # line_coordinates.append([1.0, (ix + 1) / 3, 0,0,0])
                # line_coordinates.append([1.0, (ix + 1) / 3, *up_line])



        # ix = 0
        # face_coordinate = face_coordinates[ix]
        # face = face_vertices[ix]
        # vertex_0 = vertex_palette[face[0]]
        # vertex_1 = vertex_palette[face[1]]
        # vertex_2 = vertex_palette[face[2]]
        # print(ix, vertex_0, vertex_1, vertex_2)
        # line_coordinates.append(face_coordinate[0])
        # line_coordinates.append(face_coordinate[1])


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
