import numpy as np
import glm

from constants.colors import Colors
from engine.shadeable_object import ShadeableObject

EMPTY_COLOR = Colors.LIGHT_GRAY
FILL_COLOR = Colors.LIME

vertices = [
    glm.vec3(0.0, 0.0, 0.0),
    glm.vec3(0.2, 0.0, 0.0),
    glm.vec3(0.0, 0.2, 0.0),
]

PAD = 0.02

class ProgressDot(ShadeableObject):
    def __init__(self, ctx, matrix, shader, degrees):
        offset = glm.vec3(PAD, PAD, 0.0)
        match degrees:
            case 90:
                offset = glm.vec3(-PAD, PAD, 0.0)
            case 180:
                offset = glm.vec3(-PAD, -PAD, 0.0)
            case 270:
                offset = glm.vec3(PAD, -PAD, 0.0)
        transform = glm.translate(offset) * glm.rotate(
            glm.radians(degrees), glm.vec3(0, 0, 1)
        )
        vertex_array = [transform * v for v in vertices]
        super().__init__(
            ctx,
            shader,
            {"in_position": "3f"},
            np.array(vertex_array, dtype="f4"),
        )
        self.matrix = matrix
        self.done = False

    def render(self):
        uniforms = {
            "v_color": FILL_COLOR if self.done else EMPTY_COLOR,
            "m_mvp": self.matrix,
        }
        super().render(uniforms)

    def mark_done(self):
        self.done = True
