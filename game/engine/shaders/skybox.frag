#version 330 core

layout (location = 0) out vec4 frag_color;

uniform float time; // in seconds
uniform vec2 resolution;

float dist(vec2 p0, vec2 pf){
    return sqrt((pf.x-p0.x)*(pf.x-p0.x) + (pf.y-p0.y)*(pf.y-p0.y));
}

void main() {
    vec2 pos = gl_FragCoord.xy;
    float d = dist(resolution * 0.5, pos)*( sin(time / 30.0)+1.5)*0.003;
	frag_color = mix(vec4(1.0, 1.0, 1.0, 1.0), vec4(0.0, 0.0, 0.0, 1.0), d);
}
