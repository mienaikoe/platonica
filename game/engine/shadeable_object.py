import numpy as np
import moderngl as mgl
from engine.shader import get_shader_program


class ShadeableObject:

  """
    SceneObject(
      ctx,
      "line",
      {
        "u_position": "3f",
        "u_color": "3f",
      },
      [
        [0., 0., 1.],
        [1., 1., -1.],
      ]
    )
  """
  def __init__(
    self,
    ctx: mgl.Context,
    shader_name: str,
    shader_inputs: dict,
    shader_vertices: np.ndarray
  ):
    self.shader = get_shader_program(ctx, shader_name)
    buffer = self.__make_vbo(ctx, shader_vertices)

    input_sizes = []
    input_names = []
    for input_name, input_size in shader_inputs.items():
      input_sizes.append(input_size)
      input_names.append(input_name)

    self.vao= self.__make_vao(
      ctx,
      self.shader,
      [(buffer, " ".join(input_sizes), *input_names)]
    )

  def render(self, uniforms: dict):
    for key, val in uniforms.items():
      self.shader[key] = val
    self.vao.render()

  def __make_vao(self, ctx, shader, context):
    return ctx.vertex_array(shader, context)

  def __make_vbo(self, ctx, vertices):
    return ctx.buffer(np.array(vertices, dtype='f4'))

