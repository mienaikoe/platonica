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
from engine.events import FACE_ACTIVATED, FACE_ROTATED, PUZZLE_SOLVED, NEXT_PUZZLE, DONE_RESONATE, emit_face_activated, emit_event
from engine.events.mouse_click import find_face_clicked_winding


MOVEMENT_DEG_PER_DELTA = 0.005
CLICK_RADIUS = 3  # pixels

EXPLOSION_RUNTIME = 4000 # in ms
RESONATE_RUNTIME = 1000 # in ms
INTRODUCTION_RUNTIME = 4000 # ms

LINE_LUMINOSITY_INACTIVE = 0.5
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
        self.carve_shader["lumin"] = 0.0

        self.wall_shader = get_shader_program(ctx, "uniform_color")
        self.wall_shader["v_color"] = style.wall_color

        self.underside_shader = get_shader_program(ctx, "uniform_color")
        self.underside_shader["v_color"] = style.underside_color

        self.mouse_down_position = None
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

        self.is_face_rotating = False
        self.is_alive = True
        self.is_puzzle_solved = False

        self.sounds = {"rumble": SoundEffect("rumble")}

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

    def introduce(self):
        self.introduction_animator.start(0.0)

    def __update_model_matrix(self, new_transform):
        for x in range(4):
            for y in range(4):
                self.m_model[x][y] = new_transform[x][y]

    def projected_face_vertices(self) -> list[list[glm.vec4]]:
        m_mvp = self.camera.view_projection_matrix() * self.m_model
        return [face.projected_vertices(m_mvp) for face in self.faces]

    def scramble(self, face_rotations=None):
        if face_rotations is not None:
            for face_idx, rotation_amount in face_rotations.items():
                self.faces[face_idx].rotate(rotation_amount)
        else:
            for face in self.faces:
                face.scramble()

    def handle_click(self, mouse_pos):
        if self.is_face_rotating:
            return False
        clicked_face_idx = find_face_clicked_winding(
            mouse_pos, self.projected_face_vertices()
        )
        if clicked_face_idx is not None:
            emit_face_activated(clicked_face_idx)
            return True
        return False

    def set_is_resonant(self, is_resonant: bool):
        self.resonance_animator.start(
            LINE_LUMINOSITY_ACTIVE if is_resonant else LINE_LUMINOSITY_INACTIVE
        )

    def __animate_resonance(self, new_value: float):
        # self.path_color = self.base_path_color * new_value
        self.carve_shader["lumin"] = new_value

    def start_exploding(self):
        self.terrain_shader["explode"] = True
        self.terrain_shader["time"] = 0.0

    def render_exploding(self, delta_time):
        self.time += delta_time
        self.terrain_shader["time"] = self.time / 1000.0

    def stop_exploding(self):
        self.terrain_shader["explode"] = True

    def handle_events(self, delta_time: int):
        for event in pygame.event.get():
            self.handle_event(event, delta_time)

    def handle_event(self, event: pygame.event.Event, delta_time: int):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_down_position = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.mouse_down_position and not self.introduction_animator.is_animating:
                mouse_pos = pygame.mouse.get_pos()
                no_movement = (
                    math.sqrt(
                        math.pow(mouse_pos[0] - self.mouse_down_position[0], 2)
                        + math.pow(mouse_pos[1] - self.mouse_down_position[1], 2)
                    ) <= CLICK_RADIUS
                )

                if no_movement:
                    self.handle_click(pygame.mouse.get_pos())
            self.mouse_down_position = None
        elif event.type == FACE_ACTIVATED:
            face_index = event.__dict__["face_index"]
            self.is_face_rotating = True
            self.faces[face_index].rotate()
            self.sounds["rumble"].play()
        elif event.type == FACE_ROTATED:
            self.is_face_rotating = False
            is_resonant = self.puzzle.is_resonant()
            if self.is_puzzle_solved != is_resonant:
                self.is_puzzle_solved = is_resonant
                self.set_is_resonant(is_resonant)
                pygame.time.set_timer(DONE_RESONATE, RESONATE_RUNTIME, loops=1)
        elif event.type == DONE_RESONATE:
            for face in self.faces:
                face.explode()
            self.start_exploding()
            pygame.time.set_timer(PUZZLE_SOLVED, EXPLOSION_RUNTIME, loops=1)
        elif event.type == PUZZLE_SOLVED:
            # let game scene know to go to next level
            emit_event(NEXT_PUZZLE, {})
        if not self.introduction_animator.is_animating:
            self.arcball.handle_event(event)


    def render(self, delta_time: int):
        if self.introduction_animator.is_animating:
            introduction_progress = self.introduction_animator.frame(delta_time)
            self.m_model = glm.translate(
                glm.vec3(0.0, 0.0,INTRODUCTION_Z * introduction_progress)
            ) * glm.rotate(
                INTRODUCTION_ROTATION * introduction_progress,
                (0.0, 1.0, 0.0)
            )

        self.terrain_shader['m_model'].write(self.m_model)
        self.carve_shader['v_color'].write(self.style.path_color)
        if self.is_puzzle_solved:
            self.render_exploding(delta_time)
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
