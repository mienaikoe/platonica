import moderngl
import glm
import pygame
import math
import numpy as np
from constants.colors import BlendModes, Colors, ShapeStyle

from engine.camera import Camera
from engine.texture import get_texture, texture_maps
from engine.animation import AnimationLerper, AnimationLerpFunction, Animator
from engine.audio.sound_effect import SoundEffect
from puzzles.puzzle_graph import PuzzleGraph
from engine.renderable import Renderable
from engine.shader import get_shader_program
from models.types import Vertex
from models.face import Face
from engine.arcball import ArcBall
from engine.events import (
    FACE_ACTIVATED, FACE_ROTATED, ARCBALL_DONE,
    PUZZLE_SOLVED, NEXT_PUZZLE, NEXT_LEVEL, PUZZLE_EXITED,
    emit_event)
from engine.events.mouse import find_mouse_face, ClickDetector


MOVEMENT_DEG_PER_DELTA = 0.005
CLICK_RADIUS = 3  # pixels

EXPLOSION_RUNTIME = 4000 # in ms
RESONATE_RUNTIME = 1000 # in ms
INTRODUCTION_RUNTIME = 4000 # ms

ENTER_SCENE_STARTING_POS = 5.0
ENTER_SCENE_TARGET_POS = 0.0
ENTER_SCENE_RUNTIME = 2500

EXIT_SCENE_STARTING_POS = 0.0
EXIT_SCENE_TARGET_POS = -7.0
EXIT_SCENE_RUNTIME = 2500

LINE_LUMINOSITY_INACTIVE = 0.6
LINE_LUMINOSITY_ACTIVE = 1.0
INTRODUCTION_ROTATION = -np.deg2rad(360) * 2
INTRODUCTION_Z = 30


class Polyhedron(Renderable):
    def __init__(
        self,
        ctx: moderngl.Context,
        camera: Camera,
        vertices: list[list[Vertex]],
        puzzle: PuzzleGraph,
        style: ShapeStyle,
        **kwargs,
    ):
        self.puzzle = puzzle
        self.ctx = ctx
        self.camera = camera

        self.time = 0.0

        (texture, texture_location) = get_texture(ctx, style.texture_name)

        self.style = style

        self.terrain_shader = get_shader_program(ctx, "exploding_image")
        self.terrain_shader["u_texture_0"] = texture_location
        self.terrain_shader["time"] = self.time
        self.terrain_shader["run_time"] = EXPLOSION_RUNTIME
        self.terrain_shader["explode"] = False
        self.terrain_shader["v_light"].write(-camera.position)
        self.terrain_shader["v_ambient"].write(glm.vec3(0.2,0.2,0.2))

        self.carve_shader = get_shader_program(ctx, "blend_color_image")
        self.carve_shader["u_texture_0"] = texture_location
        self.carve_shader["v_color"].write(style.path_color)
        self.carve_shader["blend_mode"] = style.blend_mode
        self.carve_shader["lumin"] = LINE_LUMINOSITY_INACTIVE

        self.wall_shader = get_shader_program(ctx, "uniform_color")
        self.wall_shader["v_color"] = style.wall_color

        self.underside_shader = get_shader_program(ctx, "uniform_color")
        self.underside_shader["v_color"] = style.underside_color

        self.click_detector = ClickDetector(on_click=self.handle_click)

        self.faces = []
        puzzle_faces = puzzle.faces
        for pf in puzzle_faces:
            vs = vertices[pf.face_idx]
            face = Face(vs, pf, ctx,
                terrain_shader=self.terrain_shader,
                carve_shader=self.carve_shader,
                wall_shader=self.wall_shader,
                underside_shader=self.underside_shader,
            )
            self.faces.append(face)

        self.m_model = glm.mat4()

        self.arcball = ArcBall(self.__update_model_matrix, emit_events=kwargs.get("emit_arcball_events", False))
        self.last_model = self.m_model

        self.is_face_rotating = False
        self.is_alive = False
        self.is_puzzle_solved = False
        self.hovered_face_idx = None

        self.sounds = {
            "rumble": SoundEffect("rumble"),
            "shimmer": SoundEffect("shimmer")
        }

        self.resonance_animator = Animator(
            lerper=AnimationLerper(
                AnimationLerpFunction.linear,
                RESONATE_RUNTIME,
            ),
            start_value=LINE_LUMINOSITY_INACTIVE,
            on_frame=self.__animate_resonance,
            on_stop=self.__animate_resonance,
        )

        self.introduction_animator = Animator(
            lerper=AnimationLerper(
                AnimationLerpFunction.ease_out,
                INTRODUCTION_RUNTIME,
            ),
            start_value=1.0,
        )

        self.enter_scene_animator = Animator(
            lerper=AnimationLerper(AnimationLerpFunction.ease_out, ENTER_SCENE_RUNTIME),
            start_value=ENTER_SCENE_STARTING_POS
        )

        self.exit_scene_animator = Animator(
            lerper=AnimationLerper(AnimationLerpFunction.ease_in, EXIT_SCENE_RUNTIME),
            start_value=EXIT_SCENE_STARTING_POS,
            on_stop=self._on_exit
        )
        self.exit_scene_dx = 0


    def introduce(self):
        self.is_alive = True
        self.introduction_animator.start(0.0)

    def enter_scene(self):
        self.is_alive = True
        self.m_model = glm.translate(glm.vec3(ENTER_SCENE_STARTING_POS, 0, 0))
        self.enter_scene_animator.start(ENTER_SCENE_TARGET_POS)

    def exit_scene(self):
        self.exit_scene_dx = 0
        self.last_model = glm.mat4(self.m_model)
        self.exit_scene_animator.start(EXIT_SCENE_TARGET_POS)

    def _on_exit(self, _value):
        emit_event(PUZZLE_EXITED)

    def reset(self):
        self.is_puzzle_solved = False
        self.is_alive = False
        self.is_face_rotating = False
        self.time = 0.0
        self.resonance_animator.set(LINE_LUMINOSITY_INACTIVE)
        self.__stop_exploding()
        for face in self.faces:
            face.reset()

    def __update_model_matrix(self, new_transform):
        for x in range(4):
            for y in range(4):
                self.m_model[x][y] = new_transform[x][y]

    def projected_face_vertices(self) -> list[list[glm.vec4]]:
        m_mvp = self.camera.view_projection_matrix * self.m_model
        return [face.projected_vertices(m_mvp) for face in self.faces]

    def scramble(self, face_rotations=None):
        if face_rotations is not None:
            for face_idx, rotation_amount in face_rotations.items():
                self.faces[face_idx].rotate(rotation_amount)
        else:
            for face in self.faces:
                face.scramble()

    def handle_click(self, _mouse_pos, mouse_button: int):
        if self.is_face_rotating:
            return

        if self.hovered_face_idx is not None:
            emit_event(FACE_ACTIVATED, {
                'face_index': self.hovered_face_idx,
                'mouse_button': mouse_button,
            })

    def handle_move(self, mouse_pos):
        if self.is_puzzle_solved or self.arcball.is_dragging:
            return

        hovered_face_idx = find_mouse_face(
            mouse_pos, self.projected_face_vertices()
        )
        if hovered_face_idx != self.hovered_face_idx:
            if self.hovered_face_idx is not None:
                self.faces[self.hovered_face_idx].push()
            if hovered_face_idx is not None:
                self.faces[hovered_face_idx].pull()
            self.hovered_face_idx = hovered_face_idx

    def set_is_resonant(self, is_resonant: bool):
        if self.hovered_face_idx is not None:
            self.faces[self.hovered_face_idx].push()
        self.is_puzzle_solved = is_resonant
        self.resonance_animator.start(
            LINE_LUMINOSITY_ACTIVE if is_resonant else LINE_LUMINOSITY_INACTIVE
        )

    def __animate_resonance(self, new_value: float):
        self.carve_shader["lumin"] = new_value

    def explode(self):
        for face in self.faces:
            face.explode()
        self.__start_exploding()

    def __start_exploding(self):
        self.time = 0.0
        self.terrain_shader["explode"] = True
        self.terrain_shader["time"] = 0.0
        pygame.time.set_timer(NEXT_LEVEL, EXPLOSION_RUNTIME, loops=1)

    def __render_exploding(self, delta_time):
        self.time += delta_time
        self.terrain_shader["time"] = self.time / 1000.0

    def __stop_exploding(self):
        self.terrain_shader["explode"] = False

    def handle_event(self, event: pygame.event.Event, world_time: int):
        if not self.is_alive:
            return
        if event.type == pygame.MOUSEMOTION or event.type == ARCBALL_DONE:
            self.handle_move(pygame.mouse.get_pos())
        elif event.type == FACE_ACTIVATED:
            face_index = event.__dict__["face_index"]
            mouse_button = event.__dict__["mouse_button"]
            self.is_face_rotating = True
            if mouse_button == pygame.BUTTON_LEFT:
                self.faces[face_index].rotate(1)
            elif mouse_button == pygame.BUTTON_RIGHT:
                self.faces[face_index].rotate(-1)
            self.sounds["rumble"].play()
        elif event.type == FACE_ROTATED:
            self.is_face_rotating = False
            is_resonant = self.puzzle.is_resonant()
            if is_resonant:
                self.set_is_resonant(is_resonant)
                emit_event(PUZZLE_SOLVED)
                self.sounds["shimmer"].play()
                self.click_detector.is_enabled = False
        if not (self.introduction_animator.is_animating or
                self.enter_scene_animator.is_animating or
                self.exit_scene_animator.is_animating):
            if self.click_detector.is_enabled:
                self.click_detector.handle_event(event, world_time)
            self.arcball.handle_event(event)


    def render(self, delta_time: int):
        if not self.is_alive:
            return

        if self.introduction_animator.is_animating:
            introduction_progress = self.introduction_animator.frame(delta_time)
            self.m_model = glm.translate(
                glm.vec3(0.0, 0.0,INTRODUCTION_Z * introduction_progress)
            ) * glm.rotate(
                INTRODUCTION_ROTATION * introduction_progress,
                (0.0, 1.0, 0.0)
            )

        if self.enter_scene_animator.is_animating:
            px = self.enter_scene_animator.frame(delta_time)
            self.m_model = glm.translate(glm.vec3(px, 0, 0))

        if self.exit_scene_animator.is_animating:
            x = self.exit_scene_animator.frame(delta_time)
            self.m_model = glm.translate(glm.vec3(x, 0, -x)) * self.last_model

        self.terrain_shader['m_model'].write(self.m_model)
        self.carve_shader['v_color'].write(self.style.path_color)
        if self.is_puzzle_solved:
            self.__render_exploding(delta_time)
        for face in self.faces:
            face.renderFace(self.camera, self.m_model, delta_time)
        self.resonance_animator.frame(delta_time)

    def destroy(self):
        self.is_alive = False
        self.terrain_shader.release()
        self.carve_shader.release()
        self.wall_shader.release()
        self.underside_shader.release()
        for face in self.faces:
            face.destroy()
