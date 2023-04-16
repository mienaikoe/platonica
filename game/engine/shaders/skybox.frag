#version 330 core

layout (location = 0) out vec4 frag_color;

uniform int level;
uniform float time; // in seconds
uniform vec2 screen;

float dist(vec2 p0, vec2 pf){
    return sqrt((pf.x-p0.x)*(pf.x-p0.x) + (pf.y-p0.y)*(pf.y-p0.y));
}

vec4 lv0(){
    vec2 pos = gl_FragCoord.xy;
    vec2 origin = vec2(screen.x*0.5, screen.y*-0.1);

    vec3 bg_color = vec3(0.7059, 0.5255, 0.4314);
    vec3 core_color = vec3(0.9529, 0.7451, 0.298);

    float d = dist(origin, pos) * (sin(time)) * 0.003;
	return vec4(mix(bg_color, core_color, -d), 1.0);
}

void main() {
    if (level == 0) {
	    frag_color = lv0();
    } else {
        frag_color =  vec4(0.9, 0.9, 0.9, 1.0);
    }
}
