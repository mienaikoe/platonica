import glm
from ui.plane import Plane


class RedPlane(Plane):
    def __init__(self, ctx, camera):
        position = glm.vec2(-1, 1)
        size = glm.vec2(2.0, 0.5)
        color = glm.vec4(1.0, 0.0, 0.0, 1.0)
        super().__init__(ctx, camera, position, size, color)
