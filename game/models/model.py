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


MOVEMENT_DEG_PER_DELTA = 0.005


class Model(Renderable):
    def __init__(
        self,
        puzzle: PuzzleGraph,
        ctx: moderngl.Context,
        camera: Camera,
        texture_file_name: str
    ):
        self.puzzle = puzzle
        self.ctx = ctx
        self.camera = camera
        self.texture = get_texture(
            self.ctx,
            texture_file_name
        )
        texture_map = texture_maps[texture_file_name]
        self.texture_vertices = triangle_vertices_from_indices(
            texture_map['uv'], texture_map['faces']
        )

        self.shape_shader = get_shader_program(ctx, "image")
        self.shape_shader['u_texture_0'] = 0
        self.puzzle_shader = get_shader_program(ctx, "line")
        self.texture.use()
        self.m_model = glm.mat4()
        self.shape_vbo = self._get_shape_vbo()
        self.shape_vao = self._get_shape_vao()
        self.puzzle_vbo = self._get_puzzle_vbo()
        self.puzzle_vao = self._get_puzzle_vao()

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
        m_mvp = self.camera.projection_matrix * self.camera.view_matrix * self.m_model
        self.shape_shader["m_mvp"].write(m_mvp)
        self.puzzle_shader["m_mvp"].write(m_mvp)
        self.shape_vao.render()
        self.puzzle_vao.render(moderngl.LINES)

    def destroy(self):
        self.shape_vbo.release()
        self.puzzle_vbo.release()
        self.shape_shader.release()
        self.puzzle_shader.release()
        self.shape_vao.release()
        self.puzzle_vao.release()

    def update_model_matrix(self, new_model_matrix: np.ndarray):
        for x in range(4):
            for y in range(4):
                self.m_model[x][y] = new_model_matrix[x][y]

    def _get_shape_vao(self):
        vertex_array_object = self.ctx.vertex_array(
            self.shape_shader,
            [
                (self.shape_vbo, "2f 3f", "in_textcoord_0", "in_position"),
            ],
        )
        return vertex_array_object

    def _get_puzzle_vao(self):
        vertex_array_object = self.ctx.vertex_array(
            self.puzzle_shader,
            [
                (self.puzzle_vbo, "3f 3f", "in_color", "in_position")
            ],
        )
        return vertex_array_object

    def _get_shape_vertex_data(self):
        """
        return an np.array with shape=[L, 5] dtype='f4' (4 byte float)
        that represents the texture(uv) and vertices(xyz) of your model
        """
        pass

    def _get_puzzle_vertex_data(self):
        """
        return an np.array with shape=[L,6] dtype='f4' (4 byte float)
        that represents the vertices(xyz)(xyz) of the puzzle lines
        """
        pass

    def _get_shape_vbo(self):
        vertex_data = self._get_shape_vertex_data()
        vertex_buffer = self.ctx.buffer(vertex_data)
        return vertex_buffer

    def _get_puzzle_vbo(self):
        vertex_data = self._get_puzzle_vertex_data()
        vertex_buffer = self.ctx.buffer(vertex_data)
        return vertex_buffer

    def face_vertices(self):
        coords = self._get_shape_vertex_data()
        res = []
        m_mp = self.camera.projection_matrix * self.m_model
        for vs in coords:
            v = vs[2:]
            res.append(glm.vec3(glm.vec4(v, 1.0) * m_mp))
        return res
