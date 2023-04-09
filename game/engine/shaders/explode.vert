#version 330 core

layout(location=0)in vec4 in_position;
layout(location=1)in vec4 in_normal;

out Vertex
{
    vec4 normal;
    vec4 color;
}vertex;

uniform mat4 m_mvp;

void main(){
    gl_Position=in_position;
    vertex.normal=in_normal;
    vertex.color=vec4(.3,.6,.6,1.);
}