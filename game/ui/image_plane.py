from moderngl import Context
from engine.animation import Animator, AnimationLerper, AnimationLerpFunction
from engine.texture import get_texture
import glm
from engine.shadeable_object import ShadeableObject
from engine.renderable import Renderable
import moderngl


class ImagePlane(Renderable):
  def __init__(
    self,
    ctx: Context,
    camera_matrix: glm.mat4,
    position: glm.vec3,
    texture_filename: str,
    dimensions: glm.vec2 = glm.vec2(1.0, 1.0),
  ):
    self.ctx = ctx
    self.camera_matrix = camera_matrix
    z = position[2]
    x0 = position[0]
    x1 = position[0] + dimensions[0]
    y0 = position[1]
    y1 = position[1] + dimensions[1]
    vertices = [
      (0, 0, x0, y0, z),
      (0, 1, x0, y1, z),
      (1, 0, x1, y0, z),
      (1, 1, x1, y1, z)
    ]

    (texture, texture_location) = get_texture(self.ctx, texture_filename)

    self.image_obj = ShadeableObject(
      self.ctx,
      "image",
      {
        "in_textcoord_0": "2f",
        "in_position": "3f",
      },
      vertices
    )
    self.image_obj.shader['m_mvp'].write(
      glm.translate(
        self.camera.view_projection_matrix(),
        glm.vec3(1.0, 1.0, 0.0)
      )
    )
    self.image_obj.shader["u_texture_0"] = texture_location


  def render(self, _delta_time: int, _m_mvp: glm.mat4):
    self.image_obj.render(mode=moderngl.TRIANGLE_STRIP)

  def destroy(self):
    self.image_obj.destroy()