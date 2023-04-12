import moderngl
import glm
from ui.color_plane import ColorPlane
from constants.colors import Colors
from engine.animation import Animator, AnimationLerper, AnimationLerpFunction

FADE_IN_TIME = 3000 # ms
WHITE_RGB = Colors.WHITE.rgb

class Fader():
  def __init__(self, ctx: moderngl.Context, m_vp: glm.mat4, **kwargs):
    self.plane = ColorPlane(
        ctx,
        m_vp,
        glm.vec3(-3.0, -3.0, -2.0),
        glm.vec2(6.0,6.0),
        Colors.WHITE,
    )
    on_stop = kwargs.get("on_stop", None)
    self.animator = Animator(
        AnimationLerper(AnimationLerpFunction.ease_in, FADE_IN_TIME),
        1.0,
        on_stop=on_stop
    )

  def fade_out(self):
    self.animator.start(1.0)

  def fade_in(self):
    self.animator.start(0.0)

  def render(self, delta_time: int):
    if self.animator.is_animating:
        fade_opacity = self.animator.frame(delta_time)
        fade_color = glm.vec4(WHITE_RGB, fade_opacity)
        self.plane.render(delta_time, fade_color)
    elif self.animator.current_value == 0.0:
      # no need to render if transparent
      pass
    else:
        self.plane.render(delta_time)

  def destroy(self):
    self.plane.destroy()
