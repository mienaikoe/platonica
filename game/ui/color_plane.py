import moderngl
import glm
from engine.shader import get_shader_program
from engine.shadeable_object import ShadeableObject

from ui.plane import Plane

class ColorPlane(Plane):
    def __init__(
        self,
        ctx: moderngl.Context,
        camera_matrix,
        position: glm.vec3,
        dimensions: glm.vec2 = glm.vec2(1.0, 1.0),
        color: glm.vec4 = glm.vec4(0.0, 0.0, 0.0, 0.0),
        **kwargs
    ):
        super().__init__(ctx, camera_matrix, position, dimensions, **kwargs)
        self.obj.shader["v_color"].write(color)


    def _get_shadeable_object(self):
        return ShadeableObject(
            self.ctx,
            "uniform_color",
            {
                "in_position": "3f",
            },
            self.vertex_data
        )


    def render(self, delta_time: int, color=None):
        if color is not None:
            self.obj.shader["v_color"].write(color)
        super().render()

