#version 330 core

layout(location=0)out vec4 fragColor;

in vec2 v_uv;
in float opacity;

uniform sampler2D u_texture_0;

void main(){
    vec3 fillColor=texture(u_texture_0, v_uv).rgb;
    fragColor=vec4(fillColor, opacity);
}
