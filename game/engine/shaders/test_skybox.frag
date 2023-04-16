#ifdef GL_ES
precision mediump float;
#endif

uniform float u_time;
uniform vec2 u_resolution;

float dist(vec2 p0, vec2 pf) {
    return sqrt((pf.x - p0.x) * (pf.x - p0.x) + (pf.y - p0.y) * (pf.y - p0.y));
}

/*
vec4 lv0(float t) {
    vec2 pos = gl_FragCoord.xy;
    vec2 origin = vec2(u_resolution.x * 0.5, u_resolution.y *- 0.1);
    
    vec3 core_color = vec3(0.9294, 0.8431, 0.4824);
    vec3 bg_color = vec3(0.7059, 0.5255, 0.4314);
    
    float d = clamp(dist(origin, pos) * sin(t) * 0.003, 0.0, 1.0);
    vec3 new_color = mix(core_color, bg_color, d);
    return vec4(new_color, 1.0);
}
*/

vec4 lv1(float t) {
    vec3 c0 = vec3(0.773, 0.725, 0.682);
    vec3 c1 = vec3(0.7294, 0.7608, 0.6314);
    
    vec2 uv = gl_FragCoord.xy / u_resolution.xy;
    
    float curve = 0.1 * sin((t * uv.x) + (4.0 * uv.y));
    float d = clamp(distance(curve + uv.y, 0.5) * 1.0, 0.0, 1.0);
    float line_width = t * 0.005;
    float line_shape = smoothstep(1.0 - d, 1.0, 0.95 - line_width);
    vec3 line_color = vec3(mix(c1, c0, line_shape));
    
    return vec4(line_color, 1.0);
}

void main() {
    gl_FragColor = lv1(mod(u_time, 6.28) - 3.14);
}
