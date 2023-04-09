#version 330 core

layout(location=1)in vec3 in_position;

out vec3 f_color;

uniform vec3 v_color;
uniform mat4 m_mvp;

void main(){
  f_color=v_color;
  gl_Position=m_mvp*vec4(in_position,1.);
}