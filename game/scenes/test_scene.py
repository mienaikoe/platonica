import os
import moderngl as mgl
import pygame
import glm
from constants.colors import Colors
from constants.dimensions import SCREEN_DIMENSIONS
from puzzles.puzzle_graph import PuzzleGraph
from engine.renderable import Renderable
from models.tetra import Tetrahedron
from engine.camera import Camera


class TestScene(Renderable):
    def __init__(self, ctx: mgl.Context, switch_mode: callable):
        self.ctx = ctx
        self.switch_mode = switch_mode
        self.center = (
            SCREEN_DIMENSIONS[0] / 2,
            SCREEN_DIMENSIONS[1] / 2,
        )

    def init(self):
        self.camera = Camera(self.ctx)
        self.puzzle = PuzzleGraph.from_file_name("test-puzzle")
        texture_file_name = 'david-jorre-unsplash.png'
        self.subject = Tetrahedron(self.puzzle, self.ctx, self.camera, texture_file_name)

    def handle_click(self, mouse_pos):
        print('mouse click', mouse_pos);
        x = (2.0 * mouse_pos[0]) / SCREEN_DIMENSIONS[0] - 1.0;
        y = 1.0 - (2.0 * mouse_pos[1]) / SCREEN_DIMENSIONS[1];
        z = 1.0
        ray_nds = glm.vec3(x, y, z) # normalized coordinates
        print('norm ray', ray_nds)
        ray_clip = glm.vec4(ray_nds.xy, -1.0, 1.0) # homogen clip coord
        print('homogen clip coords', ray_clip)
        inv_proj = glm.inverse(self.camera.projection_matrix)
        print('inverse projection', inv_proj)
        ray_eye = inv_proj * ray_clip
        ray_eye = glm.vec4(ray_eye.xy, -1.0, 0.0)
        print('4d eye coordinates', ray_eye)
        ray_world = glm.normalize(glm.inverse(self.camera.view_matrix) * ray_eye).xyz
        print('ray_world', ray_world)
        # TODO nornmalize


    def handle_events(self, delta_time: int):
        self.subject.handle_events(delta_time)
        if pygame.event.get(pygame.MOUSEBUTTONDOWN) and pygame.mouse.get_pressed()[0]:
            self.handle_click(pygame.mouse.get_pos())

    def render(self, delta_time: int):
        self.ctx.clear(color=Colors.CHARCOAL)
        self.subject.render(delta_time)

    def destroy(self):
        self.subject.destroy()
