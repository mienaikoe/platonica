import os
import moderngl

dir_path = os.path.dirname(os.path.realpath(__file__))


def _get_shader_file(file_name):
  file_path = os.path.join('engine', 'shaders', file_name)
  with open(file_path, 'r') as file:
    return file.read()

def get_shader_program(ctx: moderngl.Context, shader_name: str):
  vertex_shader = _get_shader_file(f"{shader_name}.vert")
  fragment_shader = _get_shader_file(f"{shader_name}.frag")
  program = ctx.program(
      vertex_shader=vertex_shader, fragment_shader=fragment_shader
  )
  return program