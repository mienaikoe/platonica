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
        self.puzzle = PuzzleGraph.from_file_name("test-puzzle-subface")
        self.subject = Tetrahedron(self.ctx, self.camera, self.puzzle)

    def handle_events(self, delta_time: int):
        self.subject.handle_events(delta_time)

    def render(self, delta_time: int):
        self.ctx.clear(color=Colors.WHITE)
        self.subject.render(delta_time)

    def destroy(self):
        self.subject.destroy()
