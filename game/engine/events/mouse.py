import pygame
import glm
from constants.dimensions import SCREEN_DIMENSIONS
from models.types import Vertex

def screen_to_cartesian(screen_coordinates: tuple[int,int]):
    x = (2.0 * screen_coordinates[0]) / SCREEN_DIMENSIONS[0] - 1.0;
    y = 1.0 - (2.0 * screen_coordinates[1]) / SCREEN_DIMENSIONS[1];
    return (x,y)

def clip_to_screen(clip_coordinates: glm.vec4):
    # appeared to be flipped vertically, so I added "1 -" to the y coordinate
    # TODO: Still appears to bleed out. Let's try to debug this visually somehow
    return glm.vec2(
        (clip_coordinates[0] * SCREEN_DIMENSIONS[0]) / (2.0 * clip_coordinates[3]) + (SCREEN_DIMENSIONS[0] / 2),
        (-1*(clip_coordinates[1]) * SCREEN_DIMENSIONS[1]) / (2.0 * clip_coordinates[3]) + (SCREEN_DIMENSIONS[1] / 2)
    )


def find_mouse_face(mouse_pos: tuple[int, int], faces: list[list[Vertex]]):
    mouse_pos_vec = glm.vec2(mouse_pos)
    for (face_ix, face) in enumerate(faces):
        face_vec3 = [glm.vec3(vertex) for vertex in face]
        face_normal = -glm.cross(face_vec3[1] - face_vec3[0], face_vec3[2] - face_vec3[0])

        # Normals are reversed
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


CLICK_MAX_TIME = 300 # ms

class ClickDetector:
    def __init__(self, on_click: callable):
        self.mouse_down_time = None
        self.on_click = on_click

    def handle_event(self, event: pygame.event.Event, world_time: int):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_down_time = world_time

        elif event.type == pygame.MOUSEBUTTONUP:
            if self.mouse_down_time is not None and world_time - self.mouse_down_time < CLICK_MAX_TIME:
                self.on_click(
                    pygame.mouse.get_pos()
                )
            self.mouse_down_time = None

