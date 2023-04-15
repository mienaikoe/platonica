import math
import glm

from engine.animation import Animator, AnimationLerpFunction, AnimationLerper
from engine.shader import get_shader_program
from engine.shadeable_object import ShadeableObject
from constants.dimensions import SCREEN_DIMENSIONS

from ui.plane import Plane

# 30 seconds per loop

LOOP_TIME = 6000
#30000

class Skybox(Plane):
    def __init__(self, ctx, camera_matrix):
        position = glm.vec3(0, 0, 20)
        dimensions = glm.vec2(9.65, 7.25)
        super().__init__(ctx, camera_matrix, position, dimensions)
        self.obj.shader["screen"].write(glm.vec2(SCREEN_DIMENSIONS))
        self.ready = False

        self.animator = Animator(
            AnimationLerper(AnimationLerpFunction.ease_in_out, LOOP_TIME * 0.5),
            0.0, # start value
            reversible=True)
    
    def _get_shadeable_object(self):
        return ShadeableObject(
            self.ctx,
            "skybox",
            {
                "in_position": "3f",
            },
            self.vertex_data
        )
    
    def start(self, level = 0):
        self.ready = True
        self.animator.start(1.0)
        # TODO put level into uniforms

    def render(self, delta_time: int):
        if self.ready:
            t = self.animator.frame(delta_time) 
            self.obj.shader["time"] = t
            return super().render()
