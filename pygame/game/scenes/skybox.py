import math
import random
import glm

from engine.animation import Animator, AnimationLerpFunction, AnimationLerper
from engine.shader import get_shader_program
from engine.shadeable_object import ShadeableObject
from constants.dimensions import SCREEN_DIMENSIONS

from ui.plane import Plane

# 30 seconds per loop

LOOP_TIME = 30000


class Skybox(Plane):
    def __init__(self, ctx, camera_matrix):
        position = glm.vec3(0, 0, 21)
        dimensions = glm.vec2(SCREEN_DIMENSIONS)
        super().__init__(ctx, camera_matrix, position, dimensions)
        self.obj.shader["u_resolution"].write(dimensions)
        self.obj.shader["level"] = 0
        self.obj.shader["random_pos"].write(glm.vec2(random.random(), random.random()))
        self.ready = False

        self.animator = Animator(
            AnimationLerper(AnimationLerpFunction.ease_in_out, LOOP_TIME),
            -math.pi,  # start value
            reversible=True,
        )

    def _get_shadeable_object(self):
        return ShadeableObject(
            self.ctx,
            "skybox",
            {
                "in_position": "3f",
            },
            self.vertex_data,
        )

    def start(self, level=0):
        self.ready = True
        self.animator.start(math.pi)
        self.obj.shader["level"] = level

    def stop(self):
        self.animator.stop()

    def render(self, delta_time: int):
        if self.ready:
            t = self.animator.frame(delta_time)
            self.obj.shader["u_time"] = t
            return super().render()
