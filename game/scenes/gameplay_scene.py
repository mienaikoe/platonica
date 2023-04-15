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
from engine.audio.soundtrack import Soundtrack, SoundtrackSong
from engine.camera import Camera
from engine.events import NEXT_PUZZLE, emit_event, FADE_IN, FADE_OUT, FADED_OUT, PUZZLE_SOLVED, NEXT_LEVEL
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

        self.current_level_index = 0
        self.current_puzzle_index = 0
        self._load_puzzles()

        self.progress = Progress(self.ctx, camera.view_projection_matrix)
        self.soundtrack = Soundtrack()

        self.next_button = NextButton(
            self.ctx,
            self.camera.view_projection_matrix,
            glm.vec3(0, 1.2, -2.1),
            on_click=self._go_to_next_puzzle
        )
        self.next_button.set_active(False)

        self.is_last_puzzle_on_level = False
        
        self.skybox = Skybox(ctx, camera.view_projection_matrix)

    def _go_to_next_puzzle(self):
        if self.is_last_puzzle_on_level:
            self.current_puzzle().explode()
        else:
            self._end_puzzle()
        self.next_button.set_active(False)

    def init(self):
        self.soundtrack.set_song(SoundtrackSong.water)
        self.soundtrack.set_volume(0.5)
        self._start_puzzle()

    def init_music(self):
        self.soundtrack.play()

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


    def _start_puzzle(self):
        emit_event(FADE_IN)
        self.current_puzzle().introduce()

    def _end_puzzle(self):
        emit_event(FADE_OUT)

    def current_puzzle(self):
        return self.puzzles[self.current_puzzle_index]

    def advance(self):
        self.current_puzzle().destroy()
        puzzles_count = len(self.puzzles)
        if self.current_puzzle_index < puzzles_count - 1: # next puzzle
            self.current_puzzle_index += 1
            self.soundtrack.advance()
            self.is_last_puzzle_on_level = self.current_puzzle_index == puzzles_count - 1
            self._start_puzzle()
        elif self.current_level_index < len(LEVELS) - 1: # next level
            for puzzle in self.puzzles:
                puzzle.destroy()
            self.current_puzzle_index = 0
            self.current_level_index += 1
            self.progress.reset()
            self._load_puzzles()
            self.soundtrack.advance() # eventually, change song per level
            self._start_puzzle()
        else:
            self.soundtrack.advance()
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

        self.soundtrack.handle_event(event, world_time)

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
