import moderngl as mgl
import pygame

from constants.colors import Colors, set_opacity, BlendModes
from constants.dimensions import SCREEN_DIMENSIONS
from constants.shape import Shape, SHAPE_VERTICES
from puzzles.puzzle_graph import PuzzleGraph
from engine.events import NEXT_LEVEL
from engine.renderable import Renderable
from models.polyhedron import Polyhedron
from engine.camera import Camera
from ui.fader import Fader
from ui.progress import Progress

SHAPE_STYLES = {
   Shape.tetrahedron : (Colors.DARK_RED, BlendModes.Overlay),
   Shape.cube : (set_opacity(Colors.LIME, 0.8), BlendModes.Reflect),
   # colors below TBD
   Shape.octahedron: (Colors.GRAY, BlendModes.Opaque),
   Shape.dodecahedron: (Colors.GRAY, BlendModes.Opaque),
   Shape.icosahedron: (Colors.GRAY, BlendModes.Opaque),
}

LEVELS = [
    {
        "shape": Shape.tetrahedron,
        "puzzle": "4_alien",
        "texture": "david-jorre-unsplash_lighter.png",
    },
    {
        "shape": Shape.cube,
        "puzzle": "6_sudoku",
        "texture": "cube06a.png",
    },
    {
        "shape": Shape.octahedron,
        "puzzle": "8_Xs_and_Os",
        "texture": "david-jorre-unsplash_lighter.png",
    },
    {
        "shape": Shape.icosahedron,
        "puzzle": "20_stars",
        "texture": "david-jorre-unsplash_lighter.png",
    },
]


class GameplayScene(Renderable):
    def __init__(self, ctx: mgl.Context):
        self.ctx = ctx
        self.center = (
            SCREEN_DIMENSIONS[0] / 2,
            SCREEN_DIMENSIONS[1] / 2,
        )
        self.camera = Camera(self.ctx)

    def init(self):
        self.levels = []
        for level in LEVELS:
            level_poly = Polyhedron(
                self.ctx,
                self.camera,
                SHAPE_VERTICES[level["shape"]],
                PuzzleGraph.from_file_name(level["puzzle"]),
                level["texture"],
                path_style=SHAPE_STYLES[level["shape"]],
            )
            # TODO we probably want to just have a map of polyhedra and all it's properties
            # vertices, path color, blend mode, etc.
            level_poly.scramble()
            self.levels.append(level_poly)
        self.current_level_index = 0
        self.progress = Progress(self.ctx, self.camera.view_projection_matrix())
        self.fader = Fader(self.ctx, self.camera.view_projection_matrix(), on_stop=self._fade_stopped)
        self.fader.fade_in()
        self.current_level().introduce()


    def current_level(self):
        return self.levels[self.current_level_index]

    def _fade_stopped(self, _fade_amount: float):
        if self.current_level().is_puzzle_solved:
            self.advance_level()

    def fade_level(self):
        self.fader.fade_out()

    def advance_level(self):
        self.progress.complete_level(self.current_level_index)
        self.current_level().destroy()
        if self.current_level_index < len(self.levels) - 1:
            self.current_level_index += 1
            self.current_level().introduce()
            self.fader.fade_in()
        else:
            print("GAME WOM")

    def handle_event(self, event: pygame.event.Event, delta_time: int):
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(self.current_level().is_alive)
        if event.type == NEXT_LEVEL:
            print("level own detected from scene")
            self.fade_level()
        if self.current_level().is_alive:
            self.current_level().handle_event(event, delta_time)

    def render(self, delta_time: int):
        self.ctx.clear(color=Colors.WHITE)
        if self.current_level().is_alive:
            self.current_level().render(delta_time)
        self.progress.render(delta_time)
        self.fader.render(delta_time)

    def destroy(self):
        self.progress.destroy()
        self.fade_plane.destroy()
        for lvl in self.levels:
            lvl.destroy()
