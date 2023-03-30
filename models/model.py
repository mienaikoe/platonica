import os
import moderngl
import glm
import pygame
from constants.vectors import UnitVector

from engine.camera import Camera
from engine.shader import get_shader
from engine.texture import get_texture, texture_maps
from models.helpers import triangle_vertices_from_indices
from puzzles.puzzle_graph import PuzzleGraph
from engine.renderable import Renderable


MOVEMENT_DEG_PER_DELTA = 0.001


class Model(Renderable):
    def __init__(
        self,
        ctx: moderngl.Context,
        camera: Camera,
        texture_file_name: str
    ):
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
        self.shader_program = self._get_shader_program("image")
        self.shader_program['u_texture_0'] = 0
        self.texture.use()
        self.m_model = glm.mat4()
        self.vertex_buffer_object = self._get_vertex_buffer_object()
        self.vertex_array_object = self._get_vertex_array_object()


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
        self.shader_program["m_mvp"].write(
            self.camera.projection_matrix *
            self.camera.view_matrix *
            self.m_model
        )
        self.vertex_array_object.render()

    def destroy(self):
        self.vertex_buffer_object.release()
        self.shader_program.release()
        self.vertex_array_object.release()

    def _get_vertex_array_object(self):
        vertex_array_object = self.ctx.vertex_array(
            self.shader_program,
            [
                (self.vertex_buffer_object, "2f 3f", "in_textcoord_0", "in_position"),
            ],
        )
        return vertex_array_object

    def _get_vertex_data(self):
        """
        return an np.array with dtype='f4' (4 byte float)
        that represents the vertices of your model
        """
        pass

    def _get_vertex_buffer_object(self):
        vertex_data = self._get_vertex_data()
        vertex_buffer = self.ctx.buffer(vertex_data)
        return vertex_buffer

    def _get_shader_program(self, shader_name):
        vertex_shader = get_shader(f"{shader_name}.vert")
        fragment_shader = get_shader(f"{shader_name}.frag")
        program = self.ctx.program(
            vertex_shader=vertex_shader, fragment_shader=fragment_shader
        )
        return program
