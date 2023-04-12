import pygame
import moderngl
from constants.colors import Colors
from constants.dimensions import SCREEN_DIMENSIONS
from constants.shape import Shape, SHAPE_VERTICES
from ui.tutorial.path_highlight import PathHighlight
from ui.tutorial.rotation_arrow import RotationArrow
from ui.tutorial.face_highlight import FaceHighlight
from models.polyhedron import Polyhedron
from puzzles.puzzle_graph import PuzzleGraph
from engine.renderable import Renderable
from engine.camera import Camera
from engine.events import FACE_ACTIVATED, DONE_RESONATE, ARCBALL_MOVE, PUZZLE_SOLVED, SCENE_FINISH, emit_event


class TutorialScene(Renderable):
    def __init__(self, ctx: moderngl.Context):
        self.ctx = ctx
        self.center = (
            SCREEN_DIMENSIONS[0] / 2,
            SCREEN_DIMENSIONS[1] / 2,
        )
        self.tutorial_obj = None

    def init(self):
        self.camera = Camera(self.ctx)
        puzzle = PuzzleGraph.from_file_name("4_tutorial")

        self.subject = Polyhedron(
            self.ctx,
            self.camera,
            SHAPE_VERTICES[Shape.tetrahedron],
            puzzle,
            "wireframe-equilateral.png",
            emit_arcball_events=True
        )
        self.subject.scramble({2: 1})
        self.init_rotation_step()
        self.step = 0

    def handle_event(self, event: pygame.event.Event, delta_time: int):
        self.subject.handle_event(event, delta_time)
        if event.type == ARCBALL_MOVE:
          if self.step < 1:
            self.init_face_step()
            self.step = 1
        if event.type == FACE_ACTIVATED:
          if self.step < 2:
            self.init_close_step()
            self.step = 2
        elif event.type == DONE_RESONATE:
          if self.step < 3:
            self.finish()
            self.step = 4
        elif event.type == PUZZLE_SOLVED:
          print("level won")
          emit_event(SCENE_FINISH, {})

    def _destroy_tutorial_obj(self):
        if self.tutorial_obj is not None:
            self.tutorial_obj.destroy()
            self.tutorial_obj = None

    def init_rotation_step(self):
        self._destroy_tutorial_obj()
        self.tutorial_obj = RotationArrow(self.ctx, self.camera)

    def init_face_step(self):
        self._destroy_tutorial_obj()
        target_face = self.subject.faces[2]
        self.tutorial_obj = FaceHighlight(
          self.ctx,
          self.camera.view_projection_matrix(),
          target_face
        )

    def init_close_step(self):
      self._destroy_tutorial_obj()
      self.tutorial_obj = PathHighlight(
        self.ctx,
        self.camera.view_projection_matrix(),
        self.subject.faces
      )

    def finish(self):
      self._destroy_tutorial_obj()

    def render(self, delta_time: int):
        self.ctx.clear(color=Colors.WHITE)
        self.subject.render(delta_time)
        if self.tutorial_obj is not None:
          self.tutorial_obj.render(delta_time, self.subject.m_model)

    def destroy(self):
        self.subject.destroy()
