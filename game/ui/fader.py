import pygame
import moderngl
import glm
from engine.events import emit_event, FADE_IN, FADED_IN, FADE_OUT, FADED_OUT
from ui.color_plane import ColorPlane
from constants.colors import Colors
from engine.animation import Animator, AnimationLerper, AnimationLerpFunction

FADE_IN_TIME = 2000 # ms
WHITE_RGB = Colors.WHITE.rgb

class Fader():
  def __init__(self, ctx: moderngl.Context, m_vp: glm.mat4):
    self.plane = ColorPlane(
        ctx,
        m_vp,
        glm.vec3(-3.0, -3.0, -2.0),
        glm.vec2(6.0,6.0),
        Colors.WHITE,
    )
    self.animator = Animator(
        AnimationLerper(AnimationLerpFunction.ease_in, FADE_IN_TIME),
        0.0,
        on_stop=self._on_stop
    )

  def _on_stop(self, value: float):
    if value == 0.0:
      print("Faded In")
      emit_event(FADED_IN)
    elif value == 1.0:
      print("Faded Out")
      emit_event(FADED_OUT)

  def set(self, value: float):
    self.animator.current_value = value
    self.animator.target_value = value

  def handle_event(self, event: pygame.event.Event, _world_time: int):
    if event.type == FADE_IN:
      print("Fading IN")
      self.animator.start(0.0)
    elif event.type == FADE_OUT:
      print("Fading Out")
      self.animator.start(1.0)

  def render(self, delta_time: int):
    if self.animator.is_animating:
        fade_opacity = self.animator.frame(delta_time)
        fade_color = glm.vec4(WHITE_RGB, fade_opacity)
        print(fade_color)
        self.plane.render(delta_time, fade_color)
    elif self.animator.current_value == 0.0:
        # no need to render if transparent
        pass
    else:
        self.plane.render(delta_time)

  def destroy(self):
    self.plane.destroy()
