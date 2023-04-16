#version 330 core

layout(location = 0)out vec4 frag_color;

uniform int level;
uniform float u_time; // in seconds
uniform vec2 u_resolution;

float dist(vec2 p0, vec2 pf) {
    return sqrt((pf.x - p0.x) * (pf.x - p0.x) + (pf.y - p0.y) * (pf.y - p0.y));
}

vec4 lv0(float t) {
    vec2 pos = gl_FragCoord.xy;
    vec2 origin = vec2(u_resolution.x * 0.5, u_resolution.y *- 0.1);
    
    vec3 core_color = vec3(0.9686, 0.8118, 0.502);
    vec3 bg_color = vec3(0.7059, 0.5255, 0.4314);
    
    float d = clamp(dist(origin, pos) * cos(t) * 0.003, 0.0, 1.0);
    vec3 new_color = mix(core_color, bg_color, d);
    return vec4(new_color, 1.0);
}

vec4 lv1(float t) {
    vec3 colors[2] = vec3[](
        vec3(0.773, 0.725, 0.682),
        vec3(0.7294, 0.7608, 0.6314)
    );
    
    vec2 uv = gl_FragCoord.xy / u_resolution.xy;
    
    float curve = 0.1 * sin((t * uv.x) + (4.0 * uv.y));
    float d = clamp(distance(curve + uv.y, 0.5) * 1.0, 0.0, 1.0);
    float line_shape = smoothstep(1.0 - d, 1.0, 0.92);
    vec3 line_color = vec3(mix(colors[1], colors[0], line_shape));
    
    return vec4(line_color, 1.0);
}

void main() {
    if (level == 0) {
        frag_color = lv0(u_time);
    } else if (level == 1) {
        frag_color = lv1(u_time);
    } else {
        frag_color = vec4(0.9, 0.9, 0.9, 1.0);
    }
}
