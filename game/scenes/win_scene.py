import pygame
import moderngl
from constants.colors import Colors
from engine.renderable import Renderable
from engine.camera import Camera
from models.starfield import make_starfield

class WinScene(Renderable):
    def __init__(self, ctx: moderngl.Context, camera: Camera):
        self.ctx = ctx
        self.camera = camera

        self.starfield = make_starfield(ctx)


    def init(self):
      pass


    # def handle_event(self, event: pygame.event.Event, world_time: int):
    #     self.subject.handle_event(event, world_time)

    def render(self, delta_time: int):
        self.ctx.clear(color=Colors.BLACK)
        self.starfield.render()

    # def destroy(self):
    #     self.subject.destroy()
