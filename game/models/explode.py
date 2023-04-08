import os
import moderngl
import glm
import pygame
import numpy as np

from engine.vectors import normalize_vector
from engine.shader import get_shader_program
from engine.arcball import ArcBall

MOVEMENT_DEG_PER_DELTA = 0.001


class ExplodingModel:
    def __init__(self, ctx: moderngl.Context, camera, face_vertices):
        self.ctx = ctx
        self.camera = camera
        self.shader = get_shader_program(ctx, "explode")
        self.shader["run_time"] = 3
        vertices_with_normals = []
        for face in face_vertices:
            v0 = glm.vec3(face[0])
            v1 = glm.vec3(face[1])
            v2 = glm.vec3(face[2])
            midpoint = (v0 + v1 + v2) / 3
            # normal = glm.cross(v1 - v0, v2 - v0)
            vertices_with_normals.append([*v0, 1.0, *midpoint, 0.0])
            vertices_with_normals.append([*v1, 1.0, *midpoint, 0.0])
            vertices_with_normals.append([*v2, 1.0, *midpoint, 0.0])
        vertex_data = np.array(vertices_with_normals, dtype="f4")
        self.vbo = self.ctx.buffer(vertex_data)
        self.vao = self.ctx.vertex_array(
            self.shader,
            [(self.vbo, "4f 4f", "in_position", "in_normal")],
        )
        self.matrix = glm.mat4()
        self.arcball = ArcBall(self.__update_model_matrix)
        self.time = 0

    def __update_model_matrix(self, new_transform):
        for x in range(4):
            for y in range(4):
                self.matrix[x][y] = new_transform[x][y]

    def render(self, delta_time):
        m_mvp = self.camera.view_projection_matrix() * self.matrix
        self.shader["m_mvp"].write(m_mvp)
        self.time += delta_time
        self.shader["time"] = self.time / 1000
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
