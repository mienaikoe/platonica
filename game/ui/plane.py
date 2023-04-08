import moderngl
import glm
from engine.shader import get_shader_program
from engine.renderable import Renderable
import numpy as np


class Plane(Renderable):
    def __init__(
        self,
        ctx: moderngl.Context,
        camera_matrix,
        position: glm.vec2,
        dimensions: glm.vec2 = glm.vec2(1.0, 1.0),
        color: glm.vec4 = glm.vec4(0.0, 0.0, 0.0, 0.0),
    ):
        self.ctx = ctx

        self.matrix = (
            camera_matrix
            * glm.translate(glm.vec3(position.xy, 0.0))
            * glm.scale(glm.vec3(dimensions.xy, 1.0))
        )

        vertex_data = np.array(
            [
                (-1, -1, 1),  # 0
                (1, -1, 1),  # 1
                (-1, 1, 1),  # 3
                (-1, 1, 1),  # 3
                (1, -1, 1),  # 1
                (1, 1, 1),  # 2
            ],
            dtype="f4",
        )

        self.shader = get_shader_program(self.ctx, "plane")
        self.shader["color"].write(color)
        vertex_data = np.array(vertex_data, dtype="f4")
        self.vbo = self.ctx.buffer(vertex_data)
        self.vao = self.ctx.vertex_array(self.shader, [(self.vbo, "3f", "in_position")])

    def render(self, delta_time: int):
        self.shader["m_mvp"].write(self.matrix)
        self.vao.render()

    def destroy(self):
        self.vao.release()
        self.vbo.release()
