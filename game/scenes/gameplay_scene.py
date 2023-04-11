import os
import moderngl as mgl
import pygame
import glm
from constants.colors import Colors
from constants.dimensions import SCREEN_DIMENSIONS
from constants.shape import Shape, SHAPE_VERTICES
from puzzles.puzzle_graph import PuzzleGraph
from engine.events import NEXT_LEVEL
from engine.renderable import Renderable
from models.polyhedron import Polyhedron
from engine.camera import Camera
from ui.progress import Progress

LEVELS = [
        {
        "shape": Shape.tetrahedron,
        "puzzle": "4_two-diamonds",
        "texture": "david-jorre-unsplash_lighter.png",
    },
    {
        "shape": Shape.cube,
        "puzzle": "6_sudoku",
        "texture": "david-jorre-unsplash_lighter.png",
    },
    {
        "shape": Shape.octahedron,
        "puzzle": "8_Xs_and_Os",
        "texture": "david-jorre-unsplash_lighter.png",
    },
    {
        "shape": Shape.icosahedron,
        "puzzle": "20_stars",
        "texture": "david-jorre-unsplash_lighter.png",
    },
]


class GameplayScene(Renderable):
    def __init__(self, ctx: mgl.Context):
        self.ctx = ctx
        self.center = (
            SCREEN_DIMENSIONS[0] / 2,
            SCREEN_DIMENSIONS[1] / 2,
        )
        self.camera = Camera(self.ctx)

    def init(self):
        self.levels = []
        for level in LEVELS:
            level_poly = Polyhedron(
                self.ctx,
                self.camera,
                SHAPE_VERTICES[level["shape"]],
                PuzzleGraph.from_file_name(level["puzzle"]),
                level["texture"],
            )
            level_poly.scramble()
            self.levels.append(level_poly)
        self.current_level_index = 0
        self.progress = Progress(self.ctx, self.camera.view_projection_matrix())

    def current_level(self):
        return self.levels[self.current_level_index]

    def advance_level(self):
        self.progress.complete_level(self.current_level_index)
        self.current_level().destroy()
        if self.current_level_index < len(self.levels) - 1:
            self.current_level_index += 1
        else:
            print("GAME WOM")

    def handle_events(self, delta_time: int):
        if pygame.event.get(NEXT_LEVEL):
            print("level own detected from scene")
            self.advance_level()
        if self.current_level().is_alive:
            self.current_level().handle_events(delta_time)

    def render(self, delta_time: int):
        self.ctx.clear(color=Colors.WHITE)
        if self.current_level().is_alive:
            self.current_level().render(delta_time)
        self.progress.render(delta_time)

    def destroy(self):
        for lvl in self.levels:
            lvl.destroy()
