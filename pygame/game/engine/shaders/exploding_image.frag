#version 330 core

layout(location=0)out vec4 fragColor;

in vec2 v_uv;
in float opacity;
in float diffuse_lighting;

uniform sampler2D u_texture_0;
uniform vec3 v_ambient;

void main(){
    vec3 lighting = clamp(
        vec3(diffuse_lighting, diffuse_lighting, diffuse_lighting) + v_ambient,
        vec3(0.0,0.0,0.0),
        vec3(1.0, 1.0, 1.0)
    );
    vec4 textureColor = texture(u_texture_0, v_uv);
    vec3 fillColor=vec3(
        textureColor.rgb * lighting
    );
    fragColor=vec4(fillColor, opacity * textureColor.a);
}
