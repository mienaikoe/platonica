import moderngl
import glm
from engine.shader import get_shader_program
from engine.renderable import Renderable
import numpy as np


class ColorPlane(Renderable):
    def __init__(
        self,
        ctx: moderngl.Context,
        camera_matrix,
        position: glm.vec3,
        dimensions: glm.vec2 = glm.vec2(1.0, 1.0),
        color: glm.vec4 = glm.vec4(0.0, 0.0, 0.0, 0.0),
    ):
        self.ctx = ctx

        self.matrix = (
            camera_matrix
            * glm.translate(position)
            * glm.scale(glm.vec3(dimensions.xy, 1.0))
        )

        vertex_data = np.array(
            [
                (-1 , -1 , 0),  # 0
                ( 1 , -1 , 0),  # 1
                (-1 ,  1 , 0),  # 3
                ( 1 ,  1 , 0),  # 2
            ],
            dtype="f4",
        )

        self.shader = get_shader_program(self.ctx, "uniform_color")
        self.shader["v_color"].write(color)
        vertex_data = np.array(vertex_data, dtype="f4")
        self.vbo = self.ctx.buffer(vertex_data)
        self.vao = self.ctx.vertex_array(self.shader, [(self.vbo, "3f", "in_position")])

    def render(self, delta_time: int, color=None):
        if color is not None:
            self.shader["v_color"].write(color)

        self.shader["m_mvp"].write(self.matrix)
        self.vao.render(mode=moderngl.TRIANGLE_STRIP)

    def destroy(self):
        self.vbo.release()
        self.shader.release()
        self.vao.release()
