#version 330 core

layout (location = 0) in vec3 in_position;

uniform mat4 m_mvp;

void main() {
  gl_Position = m_mvp * vec4(in_position, 1.0);
}