import numpy as np
from moderngl import Context
from engine.texture import get_texture
import glm
from engine.shadeable_object import ShadeableObject

from ui.plane import Plane


UV_VERTICES = [
   (1,0), (0,0),  (1,1),(0,1),
]


class ImagePlane(Plane):
  def __init__(
    self,
    ctx: Context,
    camera_matrix: glm.mat4,
    position: glm.vec3,
    dimensions: glm.vec2,
    texture_filename: str,
    **kwargs
  ):
    super().__init__(ctx, camera_matrix, position, dimensions, **kwargs)

    (_texture, texture_location) = get_texture(self.ctx, texture_filename)
    self.obj.shader["u_texture_0"] = texture_location


  def _get_shadeable_object(self):
    return ShadeableObject(
      self.ctx,
      "image",
      {
        "in_textcoord_0": "2f",
        "in_position": "3f",
      },
      self.vertex_data
    )


  def _get_vertex_data(self):
    square_vertices = super()._get_vertex_data()
    return np.array([
        (*UV_VERTICES[ix], *square_vertices[ix])
        for ix in range(len(square_vertices))
      ],
      dtype="f4"
    )


  def render(self, delta_time: int, opacity=1.0):
    self.obj.shader['opacity'] = opacity
    super().render()
