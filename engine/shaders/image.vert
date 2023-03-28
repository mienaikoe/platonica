#version 330 core

layout (location = 0) in vec2 in_textcoord_0;
layout (location = 1) in vec3 in_position;

out vec2 uv_0;

uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;

void main() {
  uv_0 = in_textcoord_0;
  gl_Position = m_proj * m_view * m_model * vec4(in_position, 1.0);
}