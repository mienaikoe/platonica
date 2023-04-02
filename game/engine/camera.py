import glm
import moderngl

from constants.dimensions import ASPECT_RATIO
from constants.vectors import UnitVector

FOV = 50  # degrees
NEAR = 0.1
FAR = 1000


class Camera:
    def __init__(self, ctx: moderngl.Context):
        self.ctx = ctx
        self.position = glm.vec3(0, 0, -4)
        self.view_matrix = glm.lookAt(self.position, glm.vec3(0, 0, 0), UnitVector.UP)
        self.projection_matrix = glm.perspective(
            glm.radians(FOV), ASPECT_RATIO, NEAR, FAR
        )

    def view_projection_matrix(self):
        return self.projection_matrix * self.view_matrix
