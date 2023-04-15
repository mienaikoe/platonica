import moderngl
import glm
from engine.shader import get_shader_program
from engine.shadeable_object import ShadeableObject

from ui.plane import Plane

class Skybox(Plane):
    def __init__(self, ctx, camera_matrix):
        position = glm.vec3(0, 0, 20)
        dimensions = glm.vec2(10.0, 10.0)
        super().__init__(ctx, camera_matrix, position, dimensions)
        self.obj.shader["v_color"].write(glm.vec4(1.0, 1.0, 1.0, 1.0))
    
    def _get_shadeable_object(self):
        # TODO give the skybox it's own shader
        return ShadeableObject(
            self.ctx,
            "uniform_color",
            {
                "in_position": "3f",
            },
            self.vertex_data
        )
    
    def render(self, delta_time: int):
        return super().render()
