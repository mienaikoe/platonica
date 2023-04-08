import os
import moderngl as mgl
import pygame
import glm
from constants.colors import Colors
from constants.dimensions import SCREEN_DIMENSIONS
from puzzles.puzzle_graph import PuzzleGraph
from engine.events import LEVEL_WON
from engine.renderable import Renderable
from models.tetra import Tetrahedron 
from engine.camera import Camera

LEVEL_FILES = ['4_4', '4_5a', '4_6a']

class GameplayScene(Renderable):
    def __init__(self, ctx: mgl.Context, switch_mode: callable):
        self.ctx = ctx
        self.switch_mode = switch_mode
        self.center = (
            SCREEN_DIMENSIONS[0] / 2,
            SCREEN_DIMENSIONS[1] / 2,
        )
        self.camera = Camera(self.ctx)

    def init(self):
        self.levels = [ Tetrahedron(self.ctx, self.camera,
                                    PuzzleGraph.from_file_name(file)) for file in LEVEL_FILES ]
        self.current_level_index = 0
    
    def current_level(self):
        return self.levels[self.current_level_index]
    
    def advance_level(self):
        self.current_level().destroy()
        if self.current_level_index < len(self.levels) - 1:
            self.current_level_index += 1
        else:
            print('GAME WOM')

    def handle_events(self, delta_time: int):
        if pygame.event.get(LEVEL_WON):
            print('level own detected from scene')
            self.advance_level()
        if self.current_level().is_alive:
            self.current_level().handle_events(delta_time)

    def render(self, delta_time: int):
        self.ctx.clear(color=Colors.WHITE)
        if self.current_level().is_alive:
            self.current_level().render(delta_time)

    def destroy(self):
        for lvl in self.levels:
            self.lvl.destroy()

