#version 330 core

layout (location = 0) out vec4 fragColor;

vec3 white = vec3(1.0, 1.0, 1.0);

void main() {
  fragColor = vec4(white, 1.0);
}
