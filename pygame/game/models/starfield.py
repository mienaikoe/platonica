import numpy as np
import glm
import moderngl
import random
import math
from engine.shadeable_object import ShadeableObject


STARFIELD_SIZE = 300
STAR_COUNT = 500
STAR_SIZE = 0.005
STAR_DISPLACEMENT = 5


def generate_random_star_color() -> glm.vec3:
  red = random.randrange(5, 10) / 10
  blue = random.randrange(5, 10) / 10
  green = min(red, blue)

  return glm.vec3(red, green, blue)

def generate_random_star_quad() -> list[glm.vec3]:
  position = glm.vec3(
    random.randrange(-STARFIELD_SIZE,STARFIELD_SIZE) / 100,
    random.randrange(-STARFIELD_SIZE,STARFIELD_SIZE) / 100,
    STAR_DISPLACEMENT + random.randrange(-STARFIELD_SIZE,STARFIELD_SIZE) / 100,
  )

  a = position.xyz

  b = position.xyz
  b.x = b.x + STAR_SIZE

  c = position.xyz
  c.y = c.y + STAR_SIZE

  d = position.xyz
  d.x = d.x + STAR_SIZE
  d.y = d.y + STAR_SIZE

  return [
    a,b,c,
    b,c,d,
  ]



def generate_starfield_vertices():
    starfield_vertices = []
    for ix in range(STAR_COUNT):
      star_color = generate_random_star_color()
      star_vertices = generate_random_star_quad()
      for star_vertex in star_vertices:
        starfield_vertices.append([
          *star_color,
          *star_vertex
        ])
    return starfield_vertices



def make_starfield(ctx: moderngl.Context):
  return ShadeableObject(
    ctx, "vertex_color", {
      "in_color": "3f",
      "in_position": "3f"
    }, generate_starfield_vertices()
  )