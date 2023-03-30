import os

dir_path = os.path.dirname(os.path.realpath(__file__))


def get_shader(file_name):
  file_path = os.path.join('engine', 'shaders', file_name)
  with open(file_path, 'r') as file:
    return file.read()