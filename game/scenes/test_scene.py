import os
import moderngl as mgl
import pygame
import glm
from constants.colors import Colors
from constants.dimensions import SCREEN_DIMENSIONS
from puzzles.puzzle_graph import PuzzleGraph
from engine.renderable import Renderable
from models.ghost import Ghost
from models.tetra import Tetrahedron
from engine.camera import Camera
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

    def init(self):
        self.camera = Camera(self.ctx)
        self.puzzle = PuzzleGraph.from_file_name("test-puzzle")
        texture_file_name = 'david-jorre-unsplash.png'
        self.subject = Tetrahedron(self.puzzle, self.ctx, self.camera, texture_file_name)

    def handle_events(self, delta_time: int):
        self.subject.handle_events(delta_time)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                test_face_clicked(
                    pygame.mouse.get_pos(),
                    self.camera,
                    self.subject.face_vertices()
                )
            if event.type == FACE_ACTIVATED:
                print('Face picked', event.__dict__)
                # TODO handle when face is clicked


    def render(self, delta_time: int):
        self.ctx.clear(color=Colors.CHARCOAL)
        self.subject.render(delta_time)

    def destroy(self):
        self.subject.destroy()
