#version 330 core

in vec4 vertex_color;

layout(location=0)out vec4 fragColor;

void main(){
    fragColor=vertex_color;
}
