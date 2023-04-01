import os
import moderngl as mgl
import pygame
import glm
from constants.colors import Colors
from constants.dimensions import SCREEN_DIMENSIONS
from puzzles.puzzle_graph import PuzzleGraph
from engine.renderable import Renderable
from models.tetra import Tetrahedron
from engine.camera import Camera


def pointInOrOn(p1, p2, a, b):
    c1 = glm.cross(b - a, p1 - a)
    c2 = glm.cross(b - a, p2 - a)
    return glm.dot(c1, c2) >= 0

def pointInOrOnTriangle(p, a, b, c):
    test1 = pointInOrOn(p, a, b, c)
    test2 = pointInOrOn(p, b, c, a)
    test3 = pointInOrOn(p, c, a, b)
    return test1 and test2 and test3

class TestScene(Renderable):
    def __init__(self, ctx: mgl.Context, switch_mode: callable):
        self.ctx = ctx
        self.switch_mode = switch_mode
        self.center = (
            SCREEN_DIMENSIONS[0] / 2,
            SCREEN_DIMENSIONS[1] / 2,
        )

    def init(self):
        self.camera = Camera(self.ctx)
        self.puzzle = PuzzleGraph.from_file_name("test-puzzle")
        texture_file_name = 'david-jorre-unsplash.png'
        self.subject = Tetrahedron(self.puzzle, self.ctx, self.camera, texture_file_name)

    def handle_click(self, mouse_pos):
        x = (2.0 * mouse_pos[0]) / SCREEN_DIMENSIONS[0] - 1.0;
        y = 1.0 - (2.0 * mouse_pos[1]) / SCREEN_DIMENSIONS[1];
        ray_clip = glm.vec4(x, y, -1.0, 1.0) # homogen clip coord
        inv_proj = glm.inverse(self.camera.projection_matrix)
        inv_vm = glm.inverse(self.camera.view_matrix)
        ray_eye = inv_proj * ray_clip
        ray_eye4 = glm.vec4(ray_eye.xy, -1.0, 0.0)
        ray_world = (inv_vm * ray_eye4).xyz #mouse ray
        triangles = self.subject.face_vertices()
        i = 0
        f = 0
        found = -1
        while i < len(triangles):
            a = glm.vec3(triangles[i])
            b = glm.vec3(triangles[i+1])
            c = glm.vec3(triangles[i+2])

            nv = glm.cross(b - a, c - a)
            mouse_distance = glm.dot(a - self.camera.position, nv) / glm.dot(ray_world , nv)

            p = mouse_distance * ray_world + self.camera.position
            if pointInOrOnTriangle(p, a, b, c):
                found = f
                break
            f += 1
            i += 3
        if found >= 0:
            print('clicked on face', found)


    def handle_events(self, delta_time: int):
        self.subject.handle_events(delta_time)
        if pygame.event.get(pygame.MOUSEBUTTONDOWN) and pygame.mouse.get_pressed()[0]:
            self.handle_click(pygame.mouse.get_pos())

    def render(self, delta_time: int):
        self.ctx.clear(color=Colors.CHARCOAL)
        self.subject.render(delta_time)

    def destroy(self):
        self.subject.destroy()
