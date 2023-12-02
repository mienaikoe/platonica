import glm
from ui.color_plane import ColorPlane
from ui.progress_dot import ProgressDot
from engine.shader import get_shader_program
from constants.colors import Colors

class Progress(ColorPlane):
    def __init__(self, ctx, camera_matrix):
        position = glm.vec3(1.6, -1.15, -2.1)
        super().__init__(ctx, camera_matrix, position)

        shader = get_shader_program(ctx, "uniform_color")

        self.matrix = (self.matrix *
            glm.scale(glm.vec3(0.5, 0.5, 0.5))
        )

        self.dots = [
            ProgressDot(ctx, self.matrix, shader, 0),
            ProgressDot(ctx, self.matrix, shader, 90),
            ProgressDot(ctx, self.matrix, shader, 180),
            ProgressDot(ctx, self.matrix, shader, 270),
        ]

        self.puzzles_completed = 0
        self.empty_color = Colors.GRAY
        self.fill_color = Colors.LIME

    def set_colors(self, empty_color, fill_color):
        self.empty_color = empty_color
        self.fill_color = fill_color

    def complete_puzzle(self, index):
        self.puzzles_completed = index + 1
    
    def reset(self):
        self.puzzles_completed = 0
        for dot in self.dots:
            dot.reset()

    def render(self, delta_time: int):
        for idx, dot in enumerate(self.dots):
            color = self.fill_color if self.puzzles_completed > idx else self.empty_color
            dot.render(color)

    def destroy(self):
        self.dot.destroy()
        super().destroy()
