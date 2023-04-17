import numpy as np
import glm
import moderngl
import random
import math
from engine.shadeable_object import ShadeableObject



def generate_random_star_color() -> glm.vec3:
  red = random.randrange(5, 10) / 10
  blue = random.randrange(5, 10) / 10
  green = min(red, blue)

  return glm.vec3(red, green, blue)

def generate_random_star_position() -> glm.vec3:
  return glm.vec3(
    random.randrange(-200,200) / 100,
    random.randrange(-200,200) / 100,
    random.randrange(-200,200) / 100,
  )


def generate_starfield_vertices():
    starfield_vertices = []
    for ix in range(100):
      starfield_vertices.append([
        *generate_random_star_color(),
        *generate_random_star_position(),
      ])
    return starfield_vertices



def make_starfield(ctx: moderngl.Context):
  return ShadeableObject(
    ctx, "vertex_color", {
      "in_color": "3f",
      "in_position": "3f"
    }, generate_starfield_vertices()
  )