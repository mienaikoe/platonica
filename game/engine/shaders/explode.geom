#version 150
layout(triangles)in;
layout(triangle_strip,max_vertices=3)out;

uniform float time;// in seconds
uniform float run_time;// in seconds
uniform bool explode;
uniform mat4 m_mvp;

in Vertex
{
    vec4 normal;
    vec4 color;
}vertex[];

out vec4 vertex_color;

void main()
{
    //------ Face normal
    //
    vec3 P0=gl_in[0].gl_Position.xyz;
    vec3 P1=gl_in[1].gl_Position.xyz;
    vec3 P2=gl_in[2].gl_Position.xyz;
    
    vec3 V0=P0-P1;
    vec3 V1=P2-P1;
    
    // If the diff between V0 and V1 is too small,
    // the normal will be incorrect as well as the deformation.
    //
    vec3 diff=V1-V0;
    float diff_len=length(diff);
    
    vec3 N=normalize(cross(V1,V0));
    
    //------ Generate a new face along the direction of the face normal
    // only if diff_len is not too small.
    //
    if(length(diff_len)>.001&&explode)
    {
        int i;
        for(i=0;i<gl_in.length();i++)
        {
            vec4 P=gl_in[i].gl_Position;
            vec3 N=-1*normalize(cross(V1,V0));
            vec3 d=(time*N)+(.5*pow(time,2)*N);
            P=P+vec4(d.xyz,1.);
            gl_Position=m_mvp*P;
            float fade=1.-clamp(time/run_time,0.,1.);
            vertex_color=vec4(vertex[i].color.xyz,fade);
            EmitVertex();
        }
        EndPrimitive();
    }else{
        gl_Position=gl_in[0].gl_Position;
        vertex_color=vertex[0].color;
        EmitVertex();
        
        gl_Position=gl_in[1].gl_Position;
        vertex_color=vertex[1].color;
        EmitVertex();
        
        gl_Position=gl_in[2].gl_Position;
        vertex_color=vertex[2].color;
        EmitVertex();
        
        EndPrimitive();
    }
}