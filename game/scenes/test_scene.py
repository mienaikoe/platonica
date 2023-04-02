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
from engine.arcball import ArcBall
from engine.events import FACE_ACTIVATED
from engine.events.mouse_click import test_face_clicked

class TestScene(Renderable):
    def __init__(self, ctx: mgl.Context, switch_mode: callable):
        self.ctx = ctx
        self.switch_mode = switch_mode
        self.center = (
            SCREEN_DIMENSIONS[0] / 2,
            SCREEN_DIMENSIONS[1] / 2,
        )
        self.arcball = ArcBall()
        self.is_dragging = False

    def init(self):
        self.camera = Camera(self.ctx)
        self.puzzle = PuzzleGraph.from_file_name("test-puzzle")
        texture_file_name = 'david-jorre-unsplash.png'
        self.subject = Tetrahedron(self.puzzle, self.ctx, self.camera, texture_file_name)

    def handle_face_click(self, mouse_pos):
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
        return found >= 0

    def handle_nonface_click(self, mouse_position:  tuple[int, int]):
        self.arcball.click(mouse_position)
        self.is_dragging = True

    def handle_click(self, mouse_position: tuple[int, int]):
        on_face_click = test_face_clicked(
            mouse_position,
            self.camera,
            self.subject.face_vertices()
        )
        if on_face_click:
            return
        self.handle_nonface_click(mouse_position)

    def handle_up(self, mouse_position: tuple[int, int]):
        self.is_dragging = False

    def handle_move(self, mouse_position: tuple[int, int]):
        if not self.is_dragging:
            return
        new_transform = self.arcball.drag(mouse_position)
        self.subject.update_model_matrix(new_transform)

    def handle_events(self, delta_time: int):
        self.subject.handle_events(delta_time)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_click(pygame.mouse.get_pos())
            elif event.type == FACE_ACTIVATED:
                print('Face picked', event.__dict__)
                # TODO handle when face is clicked
            elif event.type == pygame.MOUSEBUTTONUP:
                self.handle_up(pygame.mouse.get_pos())
            elif event.type == pygame.MOUSEMOTION:
                self.handle_move(pygame.mouse.get_pos())

    def render(self, delta_time: int):
        self.ctx.clear(color=Colors.CHARCOAL)
        self.subject.render(delta_time)

    def destroy(self):
        self.subject.destroy()
