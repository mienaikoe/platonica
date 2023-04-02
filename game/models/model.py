import os
import moderngl
import glm
import pygame
import numpy as np
from constants.vectors import UnitVector

from engine.camera import Camera
from engine.texture import get_texture, texture_maps
from engine.shader import get_shader_program
from models.helpers import triangle_vertices_from_indices
from puzzles.puzzle_graph import PuzzleGraph
from engine.renderable import Renderable
from models.types import Vertex
from models.face import Face
from engine.arcball import ArcBall
from engine.events import FACE_ACTIVATED, emit_face_activated
from engine.events.mouse_click import find_face_clicked


MOVEMENT_DEG_PER_DELTA = 0.005

class Model(Renderable):
    def __init__(
        self,
        ctx: moderngl.Context,
        camera: Camera,
        vertices: list[tuple[Vertex, Vertex, Vertex]],
        puzzle: PuzzleGraph,
        # texture_file_name: str,
    ):
        self.puzzle = puzzle
        self.ctx = ctx
        self.camera = camera

        self.faces = []
        puzzle_faces = puzzle.faces
        for pf in puzzle_faces:
            vs = vertices[pf.face_idx]
            self.faces.append(Face(vs, pf, ctx))

        # self.texture = get_texture(
        #     self.ctx,
        #     texture_file_name
        # )
        # texture_map = texture_maps[texture_file_name]
        # self.texture_vertices = triangle_vertices_from_indices(
        #     texture_map['uv'], texture_map['faces']
        # )

        # self.shape_shader = get_shader_program(ctx, "image")
        # self.shape_shader['u_texture_0'] = 0
        # self.texture.use()

        # self.puzzle_shader = get_shader_program(ctx, "line")
        self.m_model = glm.mat4()
        self.arcball = ArcBall(self.__update_model_matrix)
        self.is_dragging = False
    
    def __update_model_matrix(self, new_transform):
        for x in range(4):
            for y in range(4):
                self.m_model[x][y] = new_transform[x][y]
    
    def __face_vertices(self):
        res = []
        m_mp = self.m_model
        for f in self.faces:
            vertex_group = [glm.vec3(glm.vec4(v, 1.0) * m_mp * f.matrix) for v in f.face_vertices]
            res.append(vertex_group)
        return res
    
    def handle_nonface_click(self, mouse_position:  tuple[int, int]):
        self.arcball.on_down(mouse_position)
        self.is_dragging = True

    
    def handle_click(self, mouse_pos):
        clicked_face_idx = find_face_clicked(mouse_pos, self.camera, self.__face_vertices())
        if clicked_face_idx >= 0:
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
                print('roate face', face_index)
                self.faces[face_index].rotate()
            self.arcball.handle_event(event)

    def render(self, delta_time: int):
        for face in self.faces:
            face.renderFace(self.camera, self.m_model)

    def destroy(self):
        for face in self.faces:
            face.destory()

