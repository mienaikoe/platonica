#version 150
layout(triangles)in;
layout(triangle_strip,max_vertices=3)out;

in vec4 v_normal[];

in vec2 uv[];

out vec2 v_uv;
out float opacity;
out float diffuse_lighting;

uniform float time;
uniform float run_time;
uniform bool explode;
uniform mat4 m_mvp;
uniform mat4 m_model;
uniform vec3 v_light;
uniform vec3 v_nv;

void main(){
    // bool exploding=explode[0]===1;
    vec3 P0=gl_in[0].gl_Position.xyz;
    vec3 P1=gl_in[1].gl_Position.xyz;
    vec3 P2=gl_in[2].gl_Position.xyz;
    vec3 V0=P0-P1;
    vec3 V1=P2-P1;
    
    vec3 diff=V1-V0;
    float diff_len=length(diff);
    
    vec4 v4_nv=inverse(transpose(m_model))*normalize(vec4(v_nv,0.));
    vec4 v4_light=normalize(vec4(v_light,0.));
    diffuse_lighting=clamp(
        dot(
            v4_nv,
            v4_light
        ),
        0.f,1.f
    );
    
    if(explode&&length(diff_len)>.001){
        int i;
        for(i=0;i<gl_in.length();i++)
        {
            vec4 P=gl_in[i].gl_Position;
            vec3 M=(P0+P1+P2)/3;
            vec3 d=(time*M)+(.5*pow(time,2)*M);
            P=P+vec4(d.xyz,1.);
            gl_Position=m_mvp*P;
            float fade=1.-clamp(time/run_time,0,.4);
            v_uv=uv[i];
            opacity=fade;
            EmitVertex();
        }
        EndPrimitive();
    }else{
        int i;
        for(i=0;i<gl_in.length();i++)
        {
            gl_Position=m_mvp*gl_in[i].gl_Position;
            v_uv=uv[i];
            opacity=1.;
            EmitVertex();
        }
        EndPrimitive();
    }
}