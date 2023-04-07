import moderngl
import glm
import pygame

from engine.camera import Camera
from engine.texture import get_texture, texture_maps
from puzzles.puzzle_graph import PuzzleGraph
from engine.renderable import Renderable
from models.types import Vertex
from models.face import Face
from engine.arcball import ArcBall
from engine.events import FACE_ACTIVATED, FACE_ROTATED, emit_face_activated
from engine.events.mouse_click import find_face_clicked_winding


MOVEMENT_DEG_PER_DELTA = 0.005

class Model(Renderable):
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
        texture_map = texture_maps[texture_file_name]

        self.faces = []
        puzzle_faces = puzzle.faces
        for pf in puzzle_faces:
            vs = vertices[pf.face_idx]
            uv_indices = texture_map['faces'][pf.face_idx]
            uvs = (
                texture_map['uv'][uv_indices[0]],
                texture_map['uv'][uv_indices[1]],
                texture_map['uv'][uv_indices[2]],
            )
            self.faces.append(Face(vs, pf, ctx, 0, uvs))

        self.m_model = glm.mat4()
        self.arcball = ArcBall(self.__update_model_matrix)
        self.is_dragging = False
        self.is_resonant = False

    def __update_model_matrix(self, new_transform):
        for x in range(4):
            for y in range(4):
                self.m_model[x][y] = new_transform[x][y]

    def projected_face_vertices(self) -> list[list[glm.vec4]]:
        m_mvp = self.camera.view_projection_matrix() * self.m_model
        return [face.projected_vertices(m_mvp) for face in self.faces]

    def handle_nonface_click(self, mouse_position:  tuple[int, int]):
        self.arcball.on_down(mouse_position)
        self.is_dragging = True

    def handle_click(self, mouse_pos):
        clicked_face_idx = find_face_clicked_winding(mouse_pos, self.camera, self.projected_face_vertices())
        if clicked_face_idx is not None:
            emit_face_activated(clicked_face_idx)
            return True
        return False

    def handle_events(self, delta_time: int):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_handled = self.handle_click(pygame.mouse.get_pos())
                if click_handled:
                    continue
            elif event.type == pygame.MOUSEBUTTONUP and self.is_dragging:
                self.is_dragging = False
            elif event.type == FACE_ACTIVATED:
                face_index = event.__dict__['face_index']
                self.faces[face_index].rotate()
                # TODO block face click until rotation is complete
            elif event.type == FACE_ROTATED:
                is_resonant = self.puzzle.is_resonant()
                print("Resonant", is_resonant)
                if self.is_resonant != is_resonant:
                    self.is_resonant = is_resonant
                    for face in self.faces:
                        face.set_is_resonant(is_resonant)
            self.arcball.handle_event(event)

    def render(self, delta_time: int):
        for face in self.faces:
            face.renderFace(self.camera, self.m_model, delta_time)

    def destroy(self):
        for face in self.faces:
            face.destory()

