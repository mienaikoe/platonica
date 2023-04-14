import moderngl
import pygame
import glm

from constants.colors import Colors, set_opacity, BlendModes, ShapeStyle
from constants.dimensions import SCREEN_DIMENSIONS
from constants.shape import Shape, SHAPE_VERTICES
from ui.color_plane import ColorPlane
from puzzles.puzzle_graph import PuzzleGraph
from engine.camera import Camera
from engine.events import NEXT_PUZZLE, emit_event, FADE_IN, FADE_OUT, FADED_OUT
from engine.renderable import Renderable
from models.polyhedron import Polyhedron
from ui.progress import Progress
from scenes.gameplay_levels import LEVELS


class GameplayScene(Renderable):
    def __init__(self, ctx: moderngl.Context, camera: Camera):
        self.ctx = ctx
        self.camera = camera
        self.center = (
            SCREEN_DIMENSIONS[0] / 2,
            SCREEN_DIMENSIONS[1] / 2,
        )

        self.current_level_index = 0
        self.current_puzzle_index = 0
        self._load_puzzles()

        self.progress = Progress(self.ctx, camera.view_projection_matrix)
        # Example of a button
        # self.button = ColorPlane(
        #     self.ctx,
        #     self.camera.view_projection_matrix,
        #     position=glm.vec3(1.6, -1.15, -2.1),
        #     dimensions=glm.vec2(1.0,1.0),
        #     color=Colors.LIME,
        #     on_click=self._on_click
        # )

    # def _on_click(self):
    #     print("hiii")


    def init(self):
        self._start_puzzle()

    def _load_puzzles(self):
        level = LEVELS[self.current_level_index]
        self.puzzles = []
        puzzles_in_level = level['puzzles']
        puzzles_count = len(puzzles_in_level)
        for index, puzzle in enumerate(puzzles_in_level):
            level_poly = Polyhedron(
                self.ctx,
                self.camera,
                SHAPE_VERTICES[level["shape"]],
                PuzzleGraph.from_file_name(puzzle),
                style=level["style"],
                is_last_puzzle=(index == puzzles_count - 1)
            )
            level_poly.scramble()
            self.puzzles.append(level_poly)


    def _start_puzzle(self):
        emit_event(FADE_IN)
        self.current_puzzle().introduce()

    def _end_puzzle(self):
        emit_event(FADE_OUT)

    def current_puzzle(self):
        return self.puzzles[self.current_puzzle_index]

    def advance(self):
        self.current_puzzle().destroy()
        if self.current_puzzle_index < len(self.puzzles) - 1:
            self.current_puzzle_index += 1
            self._start_puzzle()
        elif self.current_level_index < len(LEVELS) - 1:
            for puzzle in self.puzzles:
                puzzle.destroy()
            self.current_puzzle_index = 0
            self.current_level_index += 1
            self.progress.reset()
            self._load_puzzles()
            self._start_puzzle()
        else:
            print("GAME WOM")

    def handle_event(self, event: pygame.event.Event, world_time: int):
        if event.type == NEXT_PUZZLE:
            self.progress.complete_puzzle(self.current_puzzle_index)
            self._end_puzzle()
        elif event.type == FADED_OUT:
            if self.current_puzzle().is_puzzle_solved:
                self.advance()

        if self.current_puzzle().is_alive:
            self.current_puzzle().handle_event(event, world_time)

    def render(self, delta_time: int):
        if self.current_puzzle().is_alive:
            self.current_puzzle().render(delta_time)
        self.progress.render(delta_time)

    def destroy(self):
        self.progress.destroy()
        for puzzle in self.puzzles:
            puzzle.destroy()
