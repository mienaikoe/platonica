import pygame
import moderngl as mgl
from scenes.scene import Scene
from constants.mode import Mode
from constants.dimensions import SCREEN_DIMENSIONS


class GameplayScene(Scene):
    def __init__(self, ctx: mgl.Context, switch_mode: callable):
        self.ctx = ctx
        self.switch_mode = switch_mode

    def init(self):
        print("Starting New Game")

    def handle_events(self, delta_time: int):
        pass

    def render(self, delta_time: int):
        self.ctx.clear(color=(0, 0, 0))

    def destroy(self):
        pass
