import numpy as np
import moderngl
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
        ctx: moderngl.Context,
        shader: moderngl.Program | str,
        shader_inputs: dict,
        shader_vertices: np.ndarray,
    ):
        if isinstance(shader, str):
            self.shader = get_shader_program(ctx, shader)
            self.is_own_shader = True
        else:
            self.shader = shader
            self.is_own_shader = False
        buffer = self.__make_vbo(ctx, shader_vertices)

        input_sizes = []
        input_names = []
        for input_name, input_size in shader_inputs.items():
            input_sizes.append(input_size)
            input_names.append(input_name)

        self.vao = self.__make_vao(
            ctx, self.shader, [(buffer, " ".join(input_sizes), *input_names)]
        )

    def render(self, uniforms: dict):
        """
        values in uniform dict must be non-primitives.
        if you have a primative (int, float), store it in glm.vect(1)
        """
        for key, val in uniforms.items():
            self.shader[key].write(val)
        self.vao.render()

    def __make_vao(self, ctx, shader, context):
        return ctx.vertex_array(shader, context)

    def __make_vbo(self, ctx, vertices):
        return ctx.buffer(np.array(vertices, dtype="f4"))

    def set_uniform(self, uniform_name: str, uniform_value):
        self.shader[uniform_name].write(uniform_value)

    def destroy(self):
        self.vbo.release()
        self.vao.release()
        if self.is_own_shader:
            self.shader.release()
