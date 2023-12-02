#version 330 core

layout (location = 0) out vec4 fragColor;

in vec2 uv_0;

uniform sampler2D u_texture_0;
uniform float opacity;

void main() {
  vec4 textureColor = texture(u_texture_0, uv_0);
  fragColor = vec4(textureColor.rgb, opacity * textureColor.a);
}
