import os
import moderngl

dir_path = os.path.dirname(os.path.realpath(__file__))


def _get_shader_file(file_name):
  file_path = os.path.join(dir_path, 'shaders', file_name)
  if not os.path.exists(file_path):
    return None
  with open(file_path, 'r') as file:
    return file.read()

def get_shader_program(ctx: moderngl.Context, shader_name: str):
  vertex_shader = _get_shader_file(f"{shader_name}.vert")
  fragment_shader = _get_shader_file(f"{shader_name}.frag")
  geometry_shader = _get_shader_file(f"{shader_name}.geom")
  program = ctx.program(
      vertex_shader=vertex_shader,
      geometry_shader=geometry_shader,
      fragment_shader=fragment_shader
  )
  return program