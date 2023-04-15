# Example file showing a basic pygame "game loop"
import os
import pygame
import moderngl
from engine.audio.soundtrack import Soundtrack, SoundtrackSong
from engine.camera import Camera
from engine.renderable import Renderable
from scenes.tutorial_scene import TutorialScene
from scenes.gameplay_scene import GameplayScene
from scenes.test_scene import TestScene
from ui.action_menu import ActionMenu
from ui.fader import Fader
from ui.intro_plane import IntroPlane
from engine.events import SCENE_FINISH, FADE_IN, FADE_OUT, FADED_OUT, LEVEL_LOADED, PUZZLE_LOADED, emit_event


class Stage:
    def __init__(self, ctx: moderngl.Context):
        self.ctx = ctx

        # The camera matrix doesn't move in this game, so we can instantiate it here and never have to update it
        self.camera = Camera(self.ctx)

        self.tutorial = TutorialScene(self.ctx, self.camera)
        self.gameplay = GameplayScene(self.ctx, self.camera)

        if os.environ.get('SKIP_TUTORIAL', None) == '1':
            self.scene = self.gameplay
        else:
            self.scene = self.tutorial

        self.next_scene_queued = None

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

        self.soundtrack = Soundtrack()
        self.soundtrack.set_volume(0.5)

    def _to_tutorial(self):
        self.to_scene(self.tutorial)

    def _on_intro_opaque(self):
        self.scene.init()

    def _on_intro_stop(self):
        self.intro.destroy()
        self.intro = None
        if type(self.scene) == GameplayScene:
            self.scene.show_skybox()

    def queue_next_scene(self):
        if self.scene.__class__ == TutorialScene:
            self.next_scene_queued = self.gameplay
        emit_event(FADE_OUT)

    def to_scene(self, scene: Renderable):
        if self.scene != scene:
            self.scene = scene
            scene.init()

    def handle_event(self, event: pygame.event.Event, world_time: int) -> None:
        if event.type == SCENE_FINISH:
            print("Scene Finish")
            self.queue_next_scene()
        elif event.type == FADED_OUT:
            if self.next_scene_queued is not None:
                self.to_scene(self.next_scene_queued)

        self.scene.handle_event(event, world_time)
        self.fader.handle_event(event, world_time)
        self.action_menu.handle_event(event, world_time)
        self.soundtrack.handle_event(event, world_time)

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
