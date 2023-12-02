import moderngl
import glm
import pygame

from constants.colors import Colors
from ui.image_plane import ImagePlane


class ActionMenu:

  def __init__(
    self,
    ctx: moderngl.Context,
    camera_matrix: glm.mat4,
    to_tutorial: callable
  ):
    self.tutorial_button = ImagePlane(
      ctx, camera_matrix,
      glm.vec3(-1.6, -1.15, -2.1),
      glm.vec2(0.1, 0.1),
      "qmark.png",
      on_click=to_tutorial
    )

  def handle_event(self, event: pygame.event.Event, world_time: int):
    self.tutorial_button.handle_event(event, world_time)

  def render(self, delta_time: int):
    self.tutorial_button.render(delta_time)

  def destroy(self):
    self.tutorial_button.destroy()