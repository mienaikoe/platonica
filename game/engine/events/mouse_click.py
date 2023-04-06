import glm
from constants.dimensions import SCREEN_DIMENSIONS
from models.types import Vertex

# def pointInOrOn(p1, p2, a, b):
#     c1 = glm.cross(b - a, p1 - a)
#     c2 = glm.cross(b - a, p2 - a)
#     return glm.dot(c1, c2) >= 0

# def pointInOrOnTriangle(p, a, b, c):
#     test1 = pointInOrOn(p, a, b, c)
#     test2 = pointInOrOn(p, b, c, a)
#     test3 = pointInOrOn(p, c, a, b)
#     return test1 and test2 and test3

def screen_to_cartesian(screen_coordinates: tuple[int,int]):
    x = (2.0 * screen_coordinates[0]) / SCREEN_DIMENSIONS[0] - 1.0;
    y = 1.0 - (2.0 * screen_coordinates[1]) / SCREEN_DIMENSIONS[1];
    return (x,y)

def clip_to_screen(clip_coordinates: glm.vec4):
    # appeared to be flipped vertically, so I added "1 -" to the y coordinate
    # TODO: Still appears to bleed out. Let's try to debug this visually somehow
    return glm.vec2(
        (clip_coordinates[0] * SCREEN_DIMENSIONS[0]) / (2.0 * clip_coordinates[3]) + (SCREEN_DIMENSIONS[0] / 2),
        ((1 - clip_coordinates[1]) * SCREEN_DIMENSIONS[1]) / (2.0 * clip_coordinates[3]) + (SCREEN_DIMENSIONS[1] / 2)
    )

# TODO make it work for non-triangle faces
# def find_face_clicked(mouse_pos: tuple[int, int], camera, faces: list[list[glm.vec4]]):
#     (x,y) = screen_to_cartesian(mouse_pos)

#     ray_clip = glm.vec4(x, y, -1.0, 1.0) # homogen clip coord
#     inverse_projection_matrix = glm.inverse(camera.projection_matrix)
#     inverse_view_matrix = glm.inverse(camera.view_matrix)
#     ray_eye = inverse_projection_matrix * ray_clip
#     ray_eye4 = glm.vec4(ray_eye.xy, -1.0, 0.0)
#     ray_world = (inverse_view_matrix * ray_eye4).xyz #mouse ray

#     for (face_ix, face) in enumerate(faces):
#         a = face[0]
#         b = face[1]
#         c = face[2]
#         face_normal = -glm.cross(b - a, c - a)
#         if face_normal.z < 0:
#             continue
#         mouse_distance = (
#             glm.dot(a - camera.position, face_normal)
#             /
#             glm.dot(ray_world , face_normal)
#         )
#         p = mouse_distance * ray_world + camera.position
#         if pointInOrOnTriangle(p, a, b, c):
#             return face_ix
#     return None


def find_face_clicked_winding(mouse_pos: tuple[int, int], camera, faces: list[tuple['Vertex', 'Vertex', 'Vertex']]):
    mouse_pos_vec = glm.vec2(mouse_pos)
    for (face_ix, face) in enumerate(faces):
        face_vec3 = [glm.vec3(vertex) for vertex in face]
        face_normal = -glm.cross(face_vec3[1] - face_vec3[0], face_vec3[2] - face_vec3[0])
        if face_normal.z < 0:
            continue

        screen_vertices = [clip_to_screen(vertex) for vertex in face]

        point_vertex_vectors = [screen_vertex - mouse_pos_vec for screen_vertex in screen_vertices]
        angle_sum = 0
        for (ix, vector) in enumerate(point_vertex_vectors):
            next_ix = 0 if ix == len(point_vertex_vectors) - 1 else ix + 1
            next_vector = point_vertex_vectors[next_ix]
            angle = glm.acos(
                glm.dot(
                    glm.normalize(vector),
                    glm.normalize(next_vector)
                )
            )
            angle_sum += angle

        if abs(angle_sum - glm.two_pi()) < 0.1:
            return face_ix

    return None