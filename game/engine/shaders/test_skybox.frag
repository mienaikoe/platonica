#ifdef GL_ES
precision mediump float;
#endif

uniform float u_time;
uniform vec2 u_resolution;

float dist(vec2 p0, vec2 pf) {
    return sqrt((pf.x - p0.x) * (pf.x - p0.x) + (pf.y - p0.y) * (pf.y - p0.y));
}

vec4 lv0(float t) {
    vec2 pos = gl_FragCoord.xy;
    vec2 origin = vec2(u_resolution.x * 0.5, u_resolution.y *- 0.1);
    
    vec3 core_color = vec3(0.9294, 0.8431, 0.4824);
    vec3 bg_color = vec3(0.7059, 0.5255, 0.4314);
    
    float d = clamp(dist(origin, pos) * sin(t) * 0.003, 0.0, 1.0);
    vec3 new_color = mix(core_color, bg_color, d);
    return vec4(new_color, 1.0);
}

void main() {
    gl_FragColor = lv0(0.5);
}
