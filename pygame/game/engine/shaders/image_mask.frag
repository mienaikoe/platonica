#version 330 core

layout (location = 0) out vec4 fragColor;

in vec2 uv_0;

uniform vec3 u_color;
uniform sampler2D u_texture_0;

void main() {
  vec3 tex_color = texture(u_texture_0, uv_0).rgb;
  float alpha = 1.0 - tex_color[0];
  fragColor = vec4(u_color, alpha);
}
