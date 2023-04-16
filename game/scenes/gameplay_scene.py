import os
import moderngl
import pygame
import glm

from constants.colors import Colors, set_opacity, BlendModes, ShapeStyle
from constants.dimensions import SCREEN_DIMENSIONS
from constants.shape import Shape, SHAPE_VERTICES
from ui.image_plane import ImagePlane
from ui.next_button import NextButton
from puzzles.puzzle_graph import PuzzleGraph
from engine.camera import Camera
from engine.events import NEXT_PUZZLE, emit_event, FADE_IN, FADE_OUT, FADED_OUT, PUZZLE_SOLVED, NEXT_LEVEL, LEVEL_LOADED, PUZZLE_LOADED
from engine.renderable import Renderable
from models.polyhedron import Polyhedron
from ui.progress import Progress
from scenes.gameplay_levels import LEVELS
from scenes.skybox import Skybox


class GameplayScene(Renderable):
    def __init__(self, ctx: moderngl.Context, camera: Camera):
        self.ctx = ctx
        self.camera = camera
        self.center = (
            SCREEN_DIMENSIONS[0] / 2,
            SCREEN_DIMENSIONS[1] / 2,
        )

        self.progress = Progress(self.ctx, camera.view_projection_matrix)
        self.skybox = Skybox(ctx, camera.view_projection_matrix)

        self.current_level_index = 0
        self.current_puzzle_index = 0
        self._load_puzzles()


        self.next_button = NextButton(
            self.ctx,
            self.camera.view_projection_matrix,
            glm.vec3(-1.5, 0, -2.1),
            on_click=self._go_to_next_puzzle
        )
        self.next_button.set_active(False)

        self.is_last_puzzle_on_level = False

    def _go_to_next_puzzle(self):
        if self.is_last_puzzle_on_level:
            self.current_puzzle().explode()
        else:
            self._end_puzzle()
        self.next_button.set_active(False)

    def init(self):
        self._start_puzzle(True)

    def show_skybox(self):
        self.skybox.start(0)

    def _load_puzzles(self):
        level = LEVELS[self.current_level_index]
        self.puzzles = []
        puzzles_in_level = level['puzzles']
        for puzzle in puzzles_in_level:
            level_poly = Polyhedron(
                self.ctx,
                self.camera,
                SHAPE_VERTICES[level["shape"]],
                PuzzleGraph.from_file_name(puzzle),
                style=level["style"]
            )
            if os.environ.get('OVER_EASY', None) != '1':
                level_poly.scramble()
            self.puzzles.append(level_poly)
        emit_event(LEVEL_LOADED, {
            'song': level['song']
        })
        self.progress.set_colors(level["style"].wall_color, level["style"].path_color)


    def _start_puzzle(self, is_introduce = False):
        emit_event(FADE_IN)
        emit_event(PUZZLE_LOADED)
        if is_introduce:
            self.current_puzzle().introduce()
        else:
            self.current_puzzle().enter_scene()

    def _end_puzzle(self):
        if not self.is_last_puzzle_on_level:
            self.current_puzzle().exit_scene()
        emit_event(FADE_OUT)

    def current_puzzle(self):
        return self.puzzles[self.current_puzzle_index]

    def advance(self):
        self.current_puzzle().destroy()
        puzzles_count = len(self.puzzles)
        if not self.is_last_puzzle_on_level: # next puzzle
            self.current_puzzle_index += 1
            self.is_last_puzzle_on_level = self.current_puzzle_index == puzzles_count - 1
            self._start_puzzle()
        elif self.current_level_index < len(LEVELS) - 1: # next level
            for puzzle in self.puzzles:
                puzzle.destroy()
            self.current_puzzle_index = 0
            self.current_level_index += 1
            self.progress.reset()
            self._load_puzzles()
            self._start_puzzle(True)
            self.skybox.start(self.current_level_index)
        else:
            print("GAME WOM")

    def handle_event(self, event: pygame.event.Event, world_time: int):
        if event.type == PUZZLE_SOLVED:
            self.progress.complete_puzzle(self.current_puzzle_index)
            self.next_button.set_active(True)
        elif event.type == NEXT_PUZZLE:
            self._end_puzzle()
        elif event.type == FADED_OUT or event.type == NEXT_LEVEL:
            if self.current_puzzle().is_puzzle_solved:
                self.advance()

        if self.current_puzzle().is_alive:
            self.current_puzzle().handle_event(event, world_time)

        self.next_button.handle_event(event, world_time)


    def render(self, delta_time: int):
        self.skybox.render(delta_time)
        if self.current_puzzle().is_alive:
            self.current_puzzle().render(delta_time)
        self.progress.render(delta_time)
        if self.next_button.is_active():
            self.next_button.render(delta_time)

    def destroy(self):
        self.progress.destroy()
        for puzzle in self.puzzles:
            puzzle.destroy()
