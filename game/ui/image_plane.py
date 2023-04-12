import numpy as np
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
    dimensions: glm.vec2,
    texture_filename: str,
  ):
    self.ctx = ctx

    self.matrix = (
        camera_matrix
        * glm.translate(position)
        * glm.scale(glm.vec3(dimensions.xy, 1.0))
    )

    vertex_data = np.array(
        [
            (0, 0, 1 , -1 , 0),  # 0
            (0, 1,  1 , 1 , 0),  # 1
            (1, 0, -1 ,  -1 , 0),  # 3
            (1, 1,  -1 ,  1 , 0),  # 2
        ],
        dtype="f4",
    )

    (texture, texture_location) = get_texture(self.ctx, texture_filename)

    self.image_obj = ShadeableObject(
      self.ctx,
      "image",
      {
        "in_textcoord_0": "2f",
        "in_position": "3f",
      },
      vertex_data
    )
    self.image_obj.shader["m_mvp"].write(self.matrix)
    self.image_obj.shader["u_texture_0"] = texture_location


  def render(self, delta_time: int, opacity=1.0):
    self.image_obj.shader['opacity'] = opacity
    self.image_obj.render(mode=moderngl.TRIANGLE_STRIP)

  def destroy(self):
    self.image_obj.destroy()