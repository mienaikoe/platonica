import moderngl as mgl
from constants.colors import Colors
from constants.dimensions import SCREEN_DIMENSIONS
from engine.renderable import Renderable
from constants.mode import Mode
from models.cube import Cube
from models.tetra import Tetrahedron
from engine.camera import Camera

button_dimensions = (160, 40)
button_margin = 20


class MenuScene(Renderable):
    def __init__(self, ctx: mgl.Context, switch_mode: callable):
        self.ctx = ctx
        self.switch_mode = switch_mode
        self.center = (
            SCREEN_DIMENSIONS[0] / 2,
            SCREEN_DIMENSIONS[1] / 2,
        )

    def _startNewGame(self):
        self.switch_mode(Mode.GAME)

    def init(self):
        self.camera = Camera(self.ctx)
        self.subject = Tetrahedron(self.ctx, self.camera, 'tetra_tex_test.png')

    def handle_events(self, delta_time: int):
        self.subject.handle_events(delta_time)

    def render(self, delta_time: int):
        self.ctx.clear(color=Colors.CHARCOAL)
        self.subject.render(delta_time)

    def destroy(self):
        self.subject.destroy()
