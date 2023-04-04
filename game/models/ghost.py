import os
import moderngl
import glm
import pygame
import numpy as np
from constants.vectors import UnitVector

from engine.camera import Camera
from engine.shader import get_shader_program
from engine.renderable import Renderable


MOVEMENT_DEG_PER_DELTA = 0.001


class Ghost():
    def __init__(
        self,
        ctx: moderngl.Context,):
        self.ctx = ctx

        self.shader = get_shader_program(ctx, "line")
        self.vbo = None
        self.vao = None

    def set_points(self, points):
        color = (1.0, 0.0, 0.0)
        vertex_data = np.array([[*color, *v] for v in points], dtype='f4')
        self.vbo = self.ctx.buffer(vertex_data)
        self.vao = self.ctx.vertex_array(
            self.shader,
            [(self.vbo, "3f 3f", "in_color", "in_position")],
        )
    
    def draw(self, matrix: glm.mat4, mode = moderngl.LINES):
        if self.vao:
            self.shader["m_mvp"].write(matrix)
            self.vao.render(mode)

    def destroy(self):
        self.shader.release()
        if self.vao:
            self.vao.release()
        if self.vbo:
            self.vbo.release()



