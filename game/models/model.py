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

    def handle_events(self, delta_time: int):
        displacement = MOVEMENT_DEG_PER_DELTA * delta_time
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.m_model = glm.rotate(self.m_model, displacement, UnitVector.RIGHT)
        if keys[pygame.K_s]:
            self.m_model = glm.rotate(self.m_model, -displacement, UnitVector.RIGHT)
        if keys[pygame.K_d]:
            self.m_model = glm.rotate(self.m_model, displacement, UnitVector.UP)
        if keys[pygame.K_a]:
            self.m_model = glm.rotate(self.m_model, -displacement, UnitVector.UP)

    def render(self, delta_time: int):
        for face in self.faces:
            face.renderFace(self.camera, self.m_model)


    def destroy(self):
        for face in self.faces:
            face.destory()

    def update_model_matrix(self, new_model_matrix: np.ndarray):
        for x in range(4):
            for y in range(4):
                self.m_model[x][y] = new_model_matrix[x][y]

    def face_vertices(self):
        res = []
        m_mp = self.camera.projection_matrix * self.m_model
        for f in self.faces:
            vertex_group = [glm.vec3(glm.vec4(v, 1.0) * m_mp) for v in f.face_vertices]
            res.append(vertex_group)
        return res
