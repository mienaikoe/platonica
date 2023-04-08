import os
import moderngl
import glm
import pygame
import numpy as np

from engine.shader import get_shader_program
from engine.arcball import ArcBall

MOVEMENT_DEG_PER_DELTA = 0.001


class Ghost():
    def __init__(
        self,
        ctx: moderngl.Context,
        face_vertices):

        self.ctx = ctx
        self.shader = get_shader_program(ctx, "default")
        vertex_data = np.array(face_vertices, dtype='f4')
        self.vbo = self.ctx.buffer(vertex_data)
        self.vao = self.ctx.vertex_array( self.shader, [(self.vbo,  "3f", "in_position")] )
        self.matrix = glm.mat4()
        self.arcball = ArcBall(self.__update_model_matrix)

    def __update_model_matrix(self, new_transform):
        for x in range(4):
            for y in range(4):
                self.matrix[x][y] = new_transform[x][y]

    def render(self, camera):
        m_mvp = camera.view_projection_matrix() * self.matrix
        self.shader["m_mvp"].write(m_mvp)
        self.vao.render()

    def handle_events(self, delta_time: int):
        for evt in pygame.event.get():
            self.arcball.handle_event(evt)

    def destroy(self):
        self.shader.release()
        if self.vao:
            self.vao.release()
        if self.vbo:
            self.vbo.release()


