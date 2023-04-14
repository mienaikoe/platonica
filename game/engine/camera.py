import glm
import moderngl

from constants.dimensions import ASPECT_RATIO
from engine.vectors import UnitVector

FOV = 30  # degrees
NEAR = 0.1
CAMERA_DISTANCE = 7


class Camera:
    def __init__(self, ctx: moderngl.Context):
        self.ctx = ctx
        self.position = glm.vec3(0, 0, -CAMERA_DISTANCE)
        self.view_matrix = glm.lookAt(self.position, glm.vec3(0, 0, 0), UnitVector.UP)
        self.projection_matrix = glm.infinitePerspective(
            glm.radians(FOV), ASPECT_RATIO, NEAR
        )
        self.view_projection_matrix = self.projection_matrix * self.view_matrix

