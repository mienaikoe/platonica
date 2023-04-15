# Example file showing a basic pygame "game loop"
import os
import pygame
import moderngl
from engine.camera import Camera
from engine.renderable import Renderable
from scenes.tutorial_scene import TutorialScene
from scenes.gameplay_scene import GameplayScene
from scenes.test_scene import TestScene
from ui.action_menu import ActionMenu
from ui.fader import Fader
from ui.intro_plane import IntroPlane
from engine.events import SCENE_FINISH, FADE_IN, emit_event


class Stage:
    def __init__(self, ctx: moderngl.Context):
        self.ctx = ctx

        # The camera matrix doesn't move in this game, so we can instantiate it here and never have to update it
        self.camera = Camera(self.ctx)

        self.tutorial = TutorialScene(self.ctx, self.camera)
        self.gameplay = GameplayScene(self.ctx, self.camera)

        if os.environ['SKIP_TUTORIAL'] == '1':
            self.scene = self.gameplay
        else:
            self.scene = self.tutorial

        self.delta_time = 0  # Time since last frame
        self.world_time = 0  # Time since beginning of game

        camera_matrix = self.camera.view_projection_matrix

        self.fader = Fader(self.ctx, camera_matrix)
        self.action_menu = ActionMenu(self.ctx, camera_matrix, to_tutorial=self._to_tutorial)
        self.intro = IntroPlane(
            self.ctx,
            camera_matrix,
            on_opaque=self._on_intro_opaque,
            on_stop=self._on_intro_stop,
        )
        self.intro.init()

    def _to_tutorial(self):
        self.to_scene(self.tutorial)

    def _on_intro_opaque(self):
        self.scene.init()

    def _on_intro_stop(self):
        self.intro.destroy()
        self.intro = None
        self.scene.init_music()

    def next_scene(self):
        if self.scene.__class__ == TutorialScene:
            self.to_scene(self.gameplay)

    def to_scene(self, scene: Renderable):
        if self.scene != scene:
            self.scene = scene
            scene.init()

    def handle_event(self, event: pygame.event.Event, world_time: int) -> None:
        if event.type == SCENE_FINISH:
            print("Scene Finish")
            self.next_scene()
        else:
            self.scene.handle_event(event, world_time)
            self.fader.handle_event(event, world_time)
            self.action_menu.handle_event(event, world_time)

    def render(self, delta_time: int) -> None:
        if self.intro:
            self.intro.render(delta_time)

        self.scene.render(delta_time)
        self.fader.render(delta_time)
        self.action_menu.render(delta_time)

    def destroy(self):
        if self.intro:
            self.intro.destroy()
        self.scene.destroy()
        self.fader.destroy()
        self.action_menu.destroy()
