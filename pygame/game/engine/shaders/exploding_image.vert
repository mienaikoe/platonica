#version 330 core

layout(location=0)in vec2 in_textcoord_0;
layout(location=1)in vec3 in_position;

out vec2 uv;

void main(){
    uv=in_textcoord_0;
    gl_Position=vec4(in_position,1.);
}