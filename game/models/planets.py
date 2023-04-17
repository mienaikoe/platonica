import math
import random
import moderngl
import glm

from constants.shape import SHAPE_VERTICES
from engine.camera import Camera
from puzzles.puzzle_graph import PuzzleGraph
from models.polyhedron import Polyhedron
from scenes.gameplay_levels import LEVELS
from engine.animation import AnimationLerper, AnimationLerpFunction, Animator

ORIGIN = glm.vec3(0.0, 0.0, 0.0)

SCALE = 0.1


class Planet:
    def __init__(
        self,
        polyhedron: Polyhedron,
        radius: float,
        speed: float,
    ):
        self.obj = polyhedron
        self.radius = radius
        self.speed = speed

        runtime = (2 * math.pi * radius / speed) * 1000

        self.animator = Animator(
            lerper=AnimationLerper(AnimationLerpFunction.linear, runtime),
            start_value=0.0,
            infinite=True,
        )

    def start(self):
        self.animator.start(2.0 * math.pi)

    def translation_matrix(self, delta_time):
        angle = self.animator.frame(delta_time)
        t = glm.vec3(self.radius * math.cos(angle), 0, self.radius * math.sin(angle))
        return glm.translate(t)


class SolarSystem:
    def __init__(self, ctx: moderngl.Context, camera: Camera):
        self.ctx = ctx
        self.camera = camera

        self.scale_matrix = glm.scale(glm.vec3(SCALE, SCALE, SCALE))

        revolve_radius = 5
        self.planets = []
        for level in LEVELS:
            shape = level["shape"]
            puzzle = level["puzzles"][3]
            style = level["style"]
            vertices = SHAPE_VERTICES[shape]
            hedron = Polyhedron(
                self.ctx,
                self.camera,
                vertices,
                PuzzleGraph.from_file_name(puzzle),
                style=style,
                emit_arcball_events=False,
            )
            hedron.is_puzzle_solved = True
            hedron.is_alive = True
            self.planets.append(
                Planet(
                    hedron,
                    revolve_radius,
                    revolve_radius * float(random.randint(3, 6)) * 0.1,
                )
            )
            revolve_radius += random.randrange(3, 6)

    def start(self):
        for p in self.planets:
            p.start()

    def render(self, delta_time: int):
        for p in self.planets:
            p.obj.m_model = self.scale_matrix * p.translation_matrix(delta_time)
            p.obj.render(delta_time)
