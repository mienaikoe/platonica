from moderngl import Context
from engine.animation import Animator, AnimationLerper, AnimationLerpFunction
from engine.texture import get_texture
import glm
from engine.shadeable_object import ShadeableObject
from engine.renderable import Renderable
import moderngl


class RotationArrow(Renderable):
  def __init__(self, ctx: Context, camera):
    self.ctx = ctx
    self.camera = camera
    vertices = [
      (0, 0, 0, 0, 0),
      (0, 1, 0, 1, 0),
      (1, 0, 1, 0, 0),
      (1, 1, 1, 1, 0)
    ]

    (texture, texture_location) = get_texture(self.ctx, 'rotation_arrow.png')

    self.arrow = ShadeableObject(
      self.ctx,
      "image_mask",
      {
        "in_textcoord_0": "2f",
        "in_position": "3f",
      },
      vertices
    )
    self.arrow.shader['m_mvp'].write(
      glm.translate(
        self.camera.view_projection_matrix(),
        glm.vec3(1.0, 1.0, 0.0)
      ) *
      glm.scale(
        glm.vec3(0.5, 0.5, 0.5)
      )
    )
    self.arrow.shader["u_texture_0"] = texture_location
    self.arrow.shader["u_color"].write(glm.vec3(0.0, 1.0, 0.0))

    self.brightness_animator = Animator(
      AnimationLerper(AnimationLerpFunction.linear, 1000),
      0.0,
      on_stop=self._reverse_animator
    )
    self.brightness_animator.start(1.0)

  def _reverse_animator(self, old_target):
    new_target = 1.0 if old_target == 0.0 else 0.0
    self.brightness_animator.start(new_target)

  def render(self, delta_time: int, m_mvp: glm.mat4):
    brightness = self.brightness_animator.frame(delta_time)
    self.arrow.set_uniform('u_color', glm.vec3(brightness, 1.0, brightness))
    self.arrow.render(mode=moderngl.TRIANGLE_STRIP)

  def destroy(self):
    self.arrow.destroy()