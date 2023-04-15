import moderngl
import glm
from engine.shader import get_shader_program
from engine.shadeable_object import ShadeableObject
from constants.dimensions import SCREEN_DIMENSIONS

from ui.plane import Plane

# 30 seconds per loop

LOOP_TIME = 5000
#30000

class Skybox(Plane):
    def __init__(self, ctx, camera_matrix):
        position = glm.vec3(0, 0, 20)
        dimensions = glm.vec2(9.65, 7.25)
        super().__init__(ctx, camera_matrix, position, dimensions)
        self.time = 0
        self.obj.shader["screen"].write(glm.vec2(SCREEN_DIMENSIONS))
    
    def _get_shadeable_object(self):
        return ShadeableObject(
            self.ctx,
            "skybox",
            {
                "in_position": "3f",
            },
            self.vertex_data
        )
    
    def render(self, delta_time: int):
        self.time += delta_time
        if self.time > LOOP_TIME:
            self.time = 0.0
        self.obj.shader["time"] = self.time / LOOP_TIME
        return super().render()
