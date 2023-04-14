import moderngl
import glm
from engine.audio.sound_effect import SoundEffect
from ui.color_plane import ColorPlane
from ui.image_plane import ImagePlane
from constants.colors import Colors
from engine.animation import Animator, AnimationLerper, AnimationLerpFunction

DEFAULT_FADE_TIME = 2000 # ms
DEFAULT_STAY_TIME = 3000 # ms

class IntroPlane():
  def __init__(self, ctx: moderngl.Context, m_vp: glm.mat4, **kwargs):
    self.plane = ImagePlane(
        ctx,
        m_vp,
        glm.vec3(0.0, 0.0, 20.0),
        glm.vec2(8., 6.),
        "logo.png",
    )
    self.animator = Animator(
        AnimationLerper(AnimationLerpFunction.linear, kwargs.get("fade_time",DEFAULT_FADE_TIME)),
        0.0,
        on_stop=self._on_stop
    )
    self.stay_time = kwargs.get("stay_time", DEFAULT_STAY_TIME)

    self.on_stop = kwargs.get("on_stop", None)
    self.on_opaque = kwargs.get("on_opaque", None)
    self.intro_sound = SoundEffect("intro", volume=0.5)

  def _on_stop(self, opacity: float):
    if opacity == 1.0:
      if self.on_opaque:
        self.on_opaque()
      self.animator.delay(0.0, self.stay_time)
    elif self.on_stop:
      self.on_stop()

  def init(self):
    self.animator.start(1.0)
    self.intro_sound.play()

  def render(self, delta_time: int):
    if not self.plane:
      return

    if self.animator.is_animating:
      fade_opacity = self.animator.frame(delta_time)
      self.plane.render(delta_time, fade_opacity) if self.plane else None

  def destroy(self):
    self.plane.destroy()
    self.plane = None
