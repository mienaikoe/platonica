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
        self.arcball = ArcBall(self._update_model_matrix)

    def init(self):
        self.camera = Camera(self.ctx)
        self.puzzle = PuzzleGraph.from_file_name("test-puzzle")
        texture_file_name = 'david-jorre-unsplash.png'
        self.subject = Tetrahedron(self.ctx, self.camera, self.puzzle)

    def handle_nonface_click(self, mouse_position:  tuple[int, int]):
        self.arcball.on_down(mouse_position)
        self.is_dragging = True

    def handle_click(self, mouse_position: tuple[int, int]):
        return test_face_clicked(
            mouse_position,
            self.camera,
            self.subject.face_vertices()
        )

    def _update_model_matrix(self, new_transform):
        self.subject.update_model_matrix(new_transform)

    def handle_events(self, delta_time: int):
        self.subject.handle_events(delta_time)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_handled = self.handle_click(pygame.mouse.get_pos())
                if click_handled:
                    continue
            elif event.type == FACE_ACTIVATED:
                print('Face picked', event.__dict__)
                continue
                # TODO handle when face is clicked
            self.arcball.handle_event(event)

    def render(self, delta_time: int):
        self.ctx.clear(color=Colors.CHARCOAL)
        self.subject.render(delta_time)

    def destroy(self):
        self.subject.destroy()
