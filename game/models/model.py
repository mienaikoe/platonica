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
from engine.events.mouse_click import pointInOrOnTriangle
from models.ghost import Ghost
from constants.dimensions import SCREEN_DIMENSIONS


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
        self.ghost = Ghost(ctx)

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
    
    def projected_face_vertices(self):
        m_mvp = self.camera.view_projection_matrix() * self.m_model
        return [f.projected_vertices(m_mvp) for f in self.faces]
    
    def handle_nonface_click(self, mouse_position:  tuple[int, int]):
        self.arcball.on_down(mouse_position)
        self.is_dragging = True

    
    def handle_click(self, mouse_pos):
        x = (2.0 * mouse_pos[0]) / SCREEN_DIMENSIONS[0] - 1.0;
        y = 1.0 - (2.0 * mouse_pos[1]) / SCREEN_DIMENSIONS[1];
        ray_clip = glm.vec4(x, y, -1.0, 1.0) # homogen clip coord
        inv_proj = glm.inverse(self.camera.projection_matrix)
        inv_vm = glm.inverse(self.camera.view_matrix)
        ray_eye = inv_proj * ray_clip
        ray_eye4 = glm.vec4(ray_eye.xy, -1.0, 0.0)
        ray_world = (inv_vm * ray_eye4).xyz # mouse ray
        print("\t mouse", ray_world)
        f = 0
        found = -1
        faces = self.projected_face_vertices()
        points = []
        for face in faces:
            a = face[0]
            b = face[1]
            c = face[2]
            nv = glm.cross(b - a, c - a)
            center = (a + b + c) / 3
            mouse_distance = glm.dot(center - self.camera.position, nv) / glm.dot(ray_world , nv)
            p = mouse_distance * ray_world + self.camera.position
            points.append(center)
            print("face ", f)
            facing = nv.z > 0
            in_triangle = pointInOrOnTriangle(p, a, b, c)
            print('\t in tri', in_triangle, p)
            if facing and in_triangle:
                found = f
            f += 1
        self.ghost.set_points([(0, 0, 0), *points])
        if found >= 0:
            emit_face_activated(found)
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
        self.ghost.draw(self.camera.view_projection_matrix(), moderngl.LINES)

    def destroy(self):
        for face in self.faces:
            face.destory()
        self.ghost.destroy()

