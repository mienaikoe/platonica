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
from models.star import Star

ORIGIN = glm.vec3(0.0, 0.0, 0.0)

SCALE = 0.02


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
        self.angle_offset = random.random()*2*math.pi

        runtime = (2 * math.pi * radius / speed) * 1000

        self.revolve_animator = Animator(
            lerper=AnimationLerper(AnimationLerpFunction.linear, runtime),
            start_value=0.0,
            infinite=True,
        )

        self.rotate_animator = Animator(
            lerper=AnimationLerper(AnimationLerpFunction.linear, random.randint(5, 10)*1000),
            start_value=0.0,
            infinite=True,
        )


    def start(self):
        self.revolve_animator.start(2.0 * math.pi)
        self.rotate_animator.start(2.0 * math.pi)
        self.obj.set_is_resonant(True)

    def _translation_matrix(self, delta_time):
        angle = self.angle_offset + self.revolve_animator.frame(delta_time)
        t = glm.vec3(self.radius * math.cos(angle), self.radius * math.sin(angle), 0)
        return glm.translate(t)
    
    def _rotatation_matrix(self, delta_time):
        angle = self.rotate_animator.frame(delta_time)
        return glm.rotate(angle, glm.vec3(0, 0, 1))
    
    def transform_matrix(self, delta_time):
        return self._translation_matrix(delta_time) * self._rotatation_matrix(delta_time)


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
                    float(random.randint(20, 60)) / revolve_radius,
                )
            )
            revolve_radius += random.randrange(5, 10)
        self.star = Star(ctx, camera, SCALE)

    def start(self):
        for p in self.planets:
            p.start()

    def render(self, delta_time: int):
        self.star.render(delta_time)
        for p in self.planets:
            p.obj.m_model = self.scale_matrix * p.transform_matrix(delta_time)
            p.obj.render(delta_time)
