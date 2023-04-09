import glm
from ui.plane import Plane
from ui.progress_dot import ProgressDot
from engine.shader import get_shader_program


class Progress(Plane):
    def __init__(self, ctx, camera_matrix):
        position = glm.vec2(1.5, 1.5)
        super().__init__(ctx, camera_matrix, position)

        shader = get_shader_program(ctx, "uniform_color")

        self.dots = [
            ProgressDot(ctx, self.matrix, shader, 0),
            ProgressDot(ctx, self.matrix, shader, 90),
            ProgressDot(ctx, self.matrix, shader, 180),
            ProgressDot(ctx, self.matrix, shader, 270),
        ]

    def complete_level(self, index):
        self.dots[index].mark_done()

    def render(self, delta_time: int):
        for dot in self.dots:
            dot.render()

    def destroy(self):
        self.dot.destroy()
        super().destroy()
