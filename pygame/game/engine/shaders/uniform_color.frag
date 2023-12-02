#version 330 core

layout (location = 0) out vec4 frag_color;

uniform vec4 v_color;

void main() {
  frag_color = v_color;
}
