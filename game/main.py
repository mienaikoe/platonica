# Example file showing a basic pygame "game loop"
import pygame
import moderngl as mgl
from constants.dimensions import SCREEN_DIMENSIONS
from constants.colors import Colors
from engine.camera import Camera
from engine.renderable import Renderable
from stage import Stage
from scenes.tutorial_scene import TutorialScene
from scenes.gameplay_scene import GameplayScene
from scenes.test_scene import TestScene
from ui.fader import Fader
from ui.intro_plane import IntroPlane
from engine.events import PUZZLE_SOLVED, SCENE_FINISH
from dotenv import load_dotenv

load_dotenv()

MAX_FPS = 60

# Setup
pygame.init()
clock = pygame.time.Clock()

# Set OpenGL Attributes and create opengl-enabled screen
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
pygame.display.gl_set_attribute(
    pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE
)


class Main:
    def __init__(self):
        self.screen = pygame.display.set_mode(
            SCREEN_DIMENSIONS,
            flags=pygame.OPENGL | pygame.DOUBLEBUF | pygame.GL_CONTEXT_DEBUG_FLAG,
        )
        self.ctx = mgl.create_context()  # OpenGL
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.BLEND)

        self.stage = Stage(self.ctx)

        self.delta_time = 0
        self.world_time = 0

    def quit(self):
        self.scene.destroy()
        pygame.quit()
        exit()

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            else:
                print("Event", event.type)
                self.stage.handle_event(event, self.world_time)

    def render(self) -> None:
        self.ctx.clear(color=Colors.WHITE)
        self.stage.render(self.delta_time)
        pygame.display.flip()

    def run(self):
        while True:
            self.handle_events()
            self.render()
            self.delta_time = clock.tick(MAX_FPS)
            self.world_time += self.delta_time


Main().run()
