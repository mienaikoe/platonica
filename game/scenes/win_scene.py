import pygame
import moderngl
from engine.renderable import Renderable
from engine.camera import Camera


class WinScene(Renderable):
    def __init__(self, ctx: moderngl.Context, camera: Camera):
        self.ctx = ctx
        self.camera = camera

    # def handle_event(self, event: pygame.event.Event, world_time: int):
    #     self.subject.handle_event(event, world_time)

    # def render(self, delta_time: int):
    #     self.subject.render(delta_time)

    # def destroy(self):
    #     self.subject.destroy()
