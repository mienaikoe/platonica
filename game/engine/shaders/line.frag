#version 330 core

layout (location = 0) out vec4 fragColor;

in vec2 uv_0;

void main() {
  vec3 fillColor = vec3(uv_0, 1.0);
  fragColor = vec4(fillColor, 1.0);
}
