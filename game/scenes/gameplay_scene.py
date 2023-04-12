import moderngl as mgl
import pygame

from constants.colors import Colors, set_opacity, BlendModes, ShapeStyle
from constants.dimensions import SCREEN_DIMENSIONS
from constants.shape import Shape, SHAPE_VERTICES
from ui.intro_plane import IntroPlane
from puzzles.puzzle_graph import PuzzleGraph
from engine.events import NEXT_PUZZLE
from engine.renderable import Renderable
from models.polyhedron import Polyhedron
from engine.camera import Camera
from ui.fader import Fader
from ui.progress import Progress
from scenes.gameplay_levels import LEVELS



INTRO_FADE = 2000  # ms
INTRO_STAY = 2000  # ms

class GameplayScene(Renderable):
    def __init__(self, ctx: mgl.Context):
        self.ctx = ctx
        self.center = (
            SCREEN_DIMENSIONS[0] / 2,
            SCREEN_DIMENSIONS[1] / 2,
        )
        self.camera = Camera(self.ctx)
        self.current_level_index = 0
        self.current_puzzle_index = 0
        self.puzzles = []

        self.intro = IntroPlane(
            self.ctx,
            self.camera.view_projection_matrix(),
            on_stop=self._on_intro_stop,
            fade_time=INTRO_FADE,
            stay_time=INTRO_STAY,
        )
        self.progress = Progress(self.ctx, self.camera.view_projection_matrix())
        self.fader = Fader(self.ctx, self.camera.view_projection_matrix(), on_stop=self._fade_stopped)


    def init(self):
        self.intro.init()
        self._load_puzzles()
        self._start_puzzle()
        self.fader.set(0.0)

    def _on_intro_stop(self):
        self.intro.destroy()
        self.intro = None

    def _load_puzzles(self):
        level = LEVELS[self.current_level_index]
        self.puzzles = []
        for puzzle in level['puzzles']:
            level_poly = Polyhedron(
                self.ctx,
                self.camera,
                SHAPE_VERTICES[level["shape"]],
                PuzzleGraph.from_file_name(puzzle),
                style=level["style"],
            )
            # TODO we probably want to just have a map of polyhedra and all it's properties
            # vertices, path color, blend mode, etc.
            level_poly.scramble()
            self.puzzles.append(level_poly)


    def _start_puzzle(self):
        self.fader.fade_in()
        self.current_puzzle().introduce()

    def _end_puzzle(self):
        self.fader.fade_out()

    def current_puzzle(self):
        return self.puzzles[self.current_puzzle_index]

    def _fade_stopped(self, _fade_amount: float):
        if self.current_puzzle().is_puzzle_solved:
            self.advance()


    def advance(self):
        self.progress.complete_level(self.current_puzzle_index)
        self.current_puzzle().destroy()
        if self.current_puzzle_index < len(self.puzzles) - 1:
            self.current_puzzle_index += 1
            self._start_puzzle()
        elif self.current_level_index < len(LEVELS) - 1:
            for puzzle in self.puzzles:
                puzzle.destroy()
            self.current_puzzle_index = 0
            self.current_level_index += 1
            self._load_puzzles()
            self._start_puzzle()
        else:
            print("GAME WOM")

    def handle_event(self, event: pygame.event.Event, delta_time: int):
        if event.type == NEXT_PUZZLE:
            self._end_puzzle()

        if self.current_puzzle().is_alive:
            self.current_puzzle().handle_event(event, delta_time)

    def render(self, delta_time: int):
        self.ctx.clear(color=Colors.WHITE)
        if self.intro:
            if self.intro.is_opaque:
                self.current_puzzle().render(delta_time)
            self.intro.render(delta_time)
        else:
            if self.current_puzzle().is_alive:
                self.current_puzzle().render(delta_time)
            self.fader.render(delta_time)
            self.progress.render(delta_time)

    def destroy(self):
        self.progress.destroy()
        self.fader.destroy()
        for puzzle in self.puzzles:
            puzzle.destroy()
