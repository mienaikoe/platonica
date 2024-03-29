import pygame
import moderngl
import glm
from constants.colors import Colors, ShapeStyle, BlendModes
from constants.dimensions import SCREEN_DIMENSIONS
from constants.shape import Shape, SHAPE_VERTICES
from ui.tutorial.path_highlight import PathHighlight
from ui.tutorial.rotation_arrow import RotationArrow
from ui.tutorial.face_highlight import FaceHighlight
from ui.image_plane import ImagePlane
from ui.color_plane import ColorPlane
from models.polyhedron import Polyhedron
from puzzles.puzzle_graph import PuzzleGraph
from engine.renderable import Renderable
from engine.camera import Camera
from engine.events import FADE_OUT, FADED_OUT, FACE_ACTIVATED, DONE_RESONATE, ARCBALL_MOVE, PUZZLE_SOLVED, SCENE_FINISH, emit_event


class TutorialScene(Renderable):
    def __init__(self, ctx: moderngl.Context, camera: Camera):
        self.ctx = ctx
        self.camera = camera

        self.center = (
            SCREEN_DIMENSIONS[0] / 2,
            SCREEN_DIMENSIONS[1] / 2,
        )
        self.tutorial_obj = None
        self.message = None

        puzzle = PuzzleGraph.from_file_name("4_tutorial")

        self.subject = Polyhedron(
            self.ctx,
            self.camera,
            SHAPE_VERTICES[Shape.tetrahedron],
            puzzle,
            ShapeStyle(
              "wireframe-equilateral.png",
              Colors.GRAY,
              Colors.CHARCOAL,
              Colors.CHARCOAL,
              BlendModes.Multipy,
            ),
            emit_arcball_events=True
        )
        self.subject.scramble({2: 1})
        self.step = None

    def init(self):
        self.subject.reset()
        self.subject.scramble({2: 1})
        self.subject.introduce()
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
        if self.message is not None:
            self.message.destroy()
            self.message = None

    def init_rotation_step(self):
        self._destroy_tutorial_obj()
        self.message = ImagePlane(
          self.ctx,
          self.camera.view_projection_matrix,
          glm.vec3(2.6, 1.9, 2.0),
          glm.vec2(1.0, 1.0),
          'arcball-mouse.png',
        )

    def init_face_step(self):
        self._destroy_tutorial_obj()
        target_face = self.subject.faces[2]
        self.tutorial_obj = FaceHighlight(
          self.ctx,
          self.camera.view_projection_matrix,
          target_face
        )
        self.message = ImagePlane(
          self.ctx,
          self.camera.view_projection_matrix,
          glm.vec3(2.2, 1.7, 2.0),
          glm.vec2(1.0, 1.0),
          'rotate-mouse.png',
        )

    def init_close_step(self):
      self._destroy_tutorial_obj()
      self.tutorial_obj = PathHighlight(
        self.ctx,
        self.camera.view_projection_matrix,
        self.subject.faces
      )
      self.message = ImagePlane(
        self.ctx,
        self.camera.view_projection_matrix,
        glm.vec3(2.2, 1.7, 2.0),
        glm.vec2(1.0, 1.0),
        'path-edge.png',
      )

    def finish(self):
      self._destroy_tutorial_obj()
      emit_event(FADE_OUT)

    def render(self, delta_time: int):
      if self.step is not None:
        self.subject.render(delta_time)
        if self.tutorial_obj is not None:
          self.tutorial_obj.render(delta_time, self.subject.m_model)
        if self.message is not None:
          self.message.render(delta_time)

    def destroy(self):
        self.subject.destroy()
