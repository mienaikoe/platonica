#version 330 core

layout(location = 0)out vec4 frag_color;

uniform int level;
uniform vec2 random_pos;

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
    float line_width_variation = t * 0.005;
    float line_shape = smoothstep(1.0 - d, 1.0, 0.94 + line_width_variation);
    vec3 line_color = vec3(mix(colors[1], colors[0], line_shape));
    
    return vec4(line_color, 1.0);
}

vec4 lv3(float t) {
    float speed = 0.05;
    float aspect_ratio = u_resolution.y / u_resolution.x;
    vec2 uv = gl_FragCoord.xy / u_resolution.xy;
    
    vec3 color = vec3(0.3176, 0.3333, 0.4588);
    vec3 bg_color = vec3(0.2627, 0.2627, 0.3294);
    
    float x = (random_pos.x - uv.x);
    float y = (random_pos.y - uv.y) * aspect_ratio;
    
    //float r = -sqrt(x*x + y*y); //uncoment this line to symmetric ripples
    float r = - 0.5 * (x * x + y * y);
    float z = clamp(0.3 * sin((r + t * speed) / 0.02), 0.0, 1.0);
    
    vec3 ripple_color = mix(bg_color, color, z);
    return vec4(ripple_color, 1.0);
}

void main() {
    if (level == 0) {
        frag_color = lv0(u_time);
    } else if (level == 1) {
        frag_color = lv1(u_time);
    } else if (level == 3) {
        frag_color = lv3(u_time);
    } else {
        frag_color = vec4(0.9, 0.9, 0.9, 1.0);
    }
}
