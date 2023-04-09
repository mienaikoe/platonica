import moderngl
import glm
import pygame
import math

from engine.camera import Camera
from engine.texture import get_texture, texture_maps
from engine.audio.sound_effect import SoundEffect
from puzzles.puzzle_graph import PuzzleGraph
from engine.renderable import Renderable
from models.types import Vertex
from models.face import Face
from engine.arcball import ArcBall
from engine.events import FACE_ACTIVATED, FACE_ROTATED, LEVEL_WON, emit_face_activated
from engine.events.mouse_click import find_face_clicked_winding


MOVEMENT_DEG_PER_DELTA = 0.005
CLICK_RADIUS = 3  # pixels


class Polyhedron(Renderable):
    def __init__(
        self,
        ctx: moderngl.Context,
        camera: Camera,
        vertices: list[tuple[Vertex, Vertex, Vertex]],
        puzzle: PuzzleGraph,
        texture_file_name: str,
    ):
        self.puzzle = puzzle
        self.ctx = ctx
        self.camera = camera

        texture = get_texture(ctx, texture_file_name)
        texture_location = 0
        texture.use(location=texture_location)

        self.mouse_down_position = None
        self.faces = []
        puzzle_faces = puzzle.faces
        for pf in puzzle_faces:
            vs = vertices[pf.face_idx]
            face = Face(vs, pf, ctx, 0)
            face.scramble()
            self.faces.append(face)

        self.m_model = glm.mat4()
        self.arcball = ArcBall(self.__update_model_matrix)
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

    def handle_events(self, delta_time: int):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_down_position = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.mouse_down_position:
                    mouse_pos = pygame.mouse.get_pos()
                    no_movement = (
                        math.sqrt(
                            math.pow(mouse_pos[0] - self.mouse_down_position[0], 2)
                            + math.pow(mouse_pos[1] - self.mouse_down_position[1], 2)
                        )
                        <= CLICK_RADIUS
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
                    # after resonating for some time, we declare the level has been own
                    pygame.time.set_timer(LEVEL_WON, 1500, loops=1)
            self.arcball.handle_event(event)

    def render(self, delta_time: int):
        for face in self.faces:
            face.renderFace(self.camera, self.m_model, delta_time)

    def destroy(self):
        self.is_alive = False
        for face in self.faces:
            face.destroy()
