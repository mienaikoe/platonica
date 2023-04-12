#version 330 core

// Blending functions from: https://github.com/jamieowen/glsl-blend

layout (location = 0) out vec4 fragColor;

in vec2 uv_0;

uniform vec4 v_color;
uniform sampler2D u_texture_0;
uniform int blend_mode;

vec3 multiply(vec3 a, vec3 b) {
  return vec3(a[0] * b[0], a[1] * b[1], a[2] * b[2]);
}

float _overlay(float base, float blend) {
	return base<0.5?(2.0*base*blend):(1.0-2.0*(1.0-base)*(1.0-blend));
}

vec3 overlay(vec3 base, vec3 blend) {
	return vec3(_overlay(base.r,blend.r),_overlay(base.g,blend.g),_overlay(base.b,blend.b));
}

vec3 overlayWithOpacity(vec3 base, vec3 blend, float opacity) {
	return (overlay(base, blend) * opacity + base * (1.0 - opacity));
}

void main() {
  vec3 imageColor = texture(u_texture_0, uv_0).rgb;
  vec3 fillColor;
  if (blend_mode == 1) {
    fillColor = overlay(imageColor, v_color.rgb);
  } else if (blend_mode == 2) {
    fillColor = multiply(imageColor, v_color.rgb);
  } else {
    fillColor = imageColor;
  }
  fragColor = vec4(fillColor, 1.0);
}
