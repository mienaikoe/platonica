import moderngl
import glm
import pygame
import math

from engine.camera import Camera
from engine.texture import get_texture, texture_maps
from engine.audio.sound_effect import SoundEffect
from puzzles.puzzle_graph import PuzzleGraph
from engine.renderable import Renderable
from engine.shader import get_shader_program
from models.types import Vertex
from models.face import Face
from engine.arcball import ArcBall
from engine.events import FACE_ACTIVATED, FACE_ROTATED, LEVEL_WON, NEXT_LEVEL, DONE_RESONATE, emit_face_activated, emit_event
from engine.events.mouse_click import find_face_clicked_winding


MOVEMENT_DEG_PER_DELTA = 0.005
CLICK_RADIUS = 3  # pixels

EXPLOSION_RUNTIME = 4000 # in ms
RESONATE_RUNTIME = 1000 # in ms


class Polyhedron(Renderable):
    def __init__(
        self,
        ctx: moderngl.Context,
        camera: Camera,
        vertices: list[list[Vertex]],
        puzzle: PuzzleGraph,
        texture_file_name: str,
        **kwargs,
    ):
        self.puzzle = puzzle
        self.ctx = ctx
        self.camera = camera

        self.time = 0.0

        (texture, texture_location) = get_texture(ctx, texture_file_name)

        self.terrain_shader = get_shader_program(ctx, "exploding_image")
        self.terrain_shader["u_texture_0"] = texture_location
        self.terrain_shader["time"] = self.time
        self.terrain_shader["run_time"] = EXPLOSION_RUNTIME
        self.terrain_shader["explode"] = False
        self.terrain_shader["v_light"].write(-camera.position)
        self.terrain_shader["v_ambient"].write(glm.vec3(0.2,0.2,0.2))

        path_color = kwargs.get("path_color", None)

        self.mouse_down_position = None
        self.faces = []
        puzzle_faces = puzzle.faces
        for pf in puzzle_faces:
            vs = vertices[pf.face_idx]
            face = Face(vs, pf, ctx, self.terrain_shader, path_color)
            self.faces.append(face)

        self.m_model = glm.mat4()

        self.arcball = ArcBall(self.__update_model_matrix, emit_events=kwargs.get("emit_arcball_events", False))
        self.is_dragging = False

        self.is_face_rotating = False
        self.is_alive = True
        self.is_puzzle_solved = False

        self.sounds = {"rumble": SoundEffect("rumble")}

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
            if self.mouse_down_position:
                mouse_pos = pygame.mouse.get_pos()
                no_movement = (
                    math.sqrt(
                        math.pow(mouse_pos[0] - self.mouse_down_position[0], 2)
                        + math.pow(mouse_pos[1] - self.mouse_down_position[1], 2)
                    ) <= CLICK_RADIUS
                )
                self.mouse_down_position = None
                if no_movement:
                    self.handle_click(pygame.mouse.get_pos())
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
                for face in self.faces:
                    face.set_is_resonant(is_resonant)
                pygame.time.set_timer(DONE_RESONATE, RESONATE_RUNTIME, loops=1)
        elif event.type == DONE_RESONATE:
            for face in self.faces:
                face.explode()
            self.start_exploding()
            pygame.time.set_timer(LEVEL_WON, EXPLOSION_RUNTIME, loops=1)
        elif event.type == LEVEL_WON:
            # let game scene know to go to next level
            emit_event(NEXT_LEVEL, {})

        self.arcball.handle_event(event)


    def render(self, delta_time: int):
        self.terrain_shader['m_model'].write(self.m_model)
        if self.is_puzzle_solved:
            self.render_exploding(delta_time)
        for face in self.faces:
            face.renderFace(self.camera, self.m_model, delta_time)

    def destroy(self):
        self.is_alive = False
        self.terrain_shader.release()
        for face in self.faces:
            face.destroy()
