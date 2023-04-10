from moderngl import Context
from engine.animation import Animator, AnimationLerper, AnimationLerpFunction
from models.face import Face
import glm
import numpy as np
import moderngl
from engine.shadeable_object import ShadeableObject
from engine.renderable import Renderable

HIGHLIGHT_COLOR = glm.vec4(0.0, 1.0, 0.0, 0.3)

class FaceHighlight(Renderable):
  def __init__(self, ctx: Context, m_vp: glm.mat4, face: Face):
    self.m_vp = m_vp
    self.outline = ShadeableObject(
      ctx,
      "uniform_color",
      {
        "in_position": "3f",
      },
      np.array(face.face_vertices) * 1.01
    )
    self.brightness_animator = Animator(
      AnimationLerper(AnimationLerpFunction.linear, 1000),
      0.0,
      on_stop=self._reverse_animator
    )
    self.brightness_animator.start(1.0)
    self.outline.set_uniform('m_mvp', m_vp)

  def _reverse_animator(self, old_target):
    new_target = 1.0 if old_target == 0.0 else 0.0
    self.brightness_animator.start(new_target)

  def render(self, delta_time: int, m_model: glm.mat4):
    brightness = self.brightness_animator.frame(delta_time)
    self.outline.set_uniform('m_mvp', self.m_vp * m_model)
    self.outline.set_uniform('v_color', HIGHLIGHT_COLOR * brightness)
    self.outline.render()

  def destroy(self):
    self.outline.destroy()