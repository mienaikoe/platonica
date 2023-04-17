#version 330 core

layout(location = 0)out vec4 frag_color;

uniform int level;
uniform vec2 random_pos;

uniform float u_time; // in seconds
uniform vec2 u_resolution;

float dist(vec2 p0, vec2 pf) {
    return sqrt((pf.x - p0.x) * (pf.x - p0.x) + (pf.y - p0.y) * (pf.y - p0.y));
}

float clamp_normal(float i) {
    return clamp(i, 0.0, 1.0);
}

vec4 lv0(float t) {
    vec2 pos = gl_FragCoord.xy;
    vec2 origin = vec2(u_resolution.x * 0.5, u_resolution.y *- 0.1);
    
    vec3 core_color = vec3(0.9686, 0.8118, 0.502);
    vec3 bg_color = vec3(0.7059, 0.5255, 0.4314);
    
    float d = clamp_normal(dist(origin, pos) * cos(t) * 0.003);
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
    float d = clamp_normal(distance(curve + uv.y, 0.5) * 1.0);
    float line_width_variation = t * 0.005;
    float line_shape = smoothstep(1.0 - d, 1.0, 0.94 + line_width_variation);
    vec3 line_color = vec3(mix(colors[1], colors[0], line_shape));
    
    return vec4(line_color, 1.0);
}

vec4 lv2(float t) {
    vec3 base_color = vec3(0.6902, 0.9137, 0.8941);
    // vec3(0.8, 0.9333, 0.8863);
    vec3 effect_color = vec3(0.8667, 0.9686, 0.9608);
    
    vec2 uv = gl_FragCoord.xy / u_resolution.xy;
    float curve = -0.1 * tan((t * uv.y) + (3.0 * uv.x));
    float d = clamp_normal(distance(curve + uv.y, 0.5));
    float line_shape = smoothstep(1.0 - d, 1.0, 0.95);
    vec3 line_color = vec3(mix(effect_color, base_color, line_shape));
    
    return vec4(line_color, 1.0);
}

vec4 lv3(float t) {
    float speed = 0.05;
    float aspect_ratio = u_resolution.y / u_resolution.x;
    vec2 uv = gl_FragCoord.xy / u_resolution.xy;
    
    vec3 color = vec3(0.153, 0.153, 0.737);
    vec3 bg_color = vec3(0.0, 0.118, 0.353);
    
    float x = (random_pos.x - uv.x);
    float y = (random_pos.y - uv.y) * aspect_ratio;
    
    //float r = -sqrt(x*x + y*y); //uncoment this line to symmetric ripples
    float r = - 0.5 * (x * x + y * y);
    float z = clamp_normal(0.3 * sin((r + t * speed) / 0.02));
    
    vec3 ripple_color = mix(bg_color, color, z);
    return vec4(ripple_color, 1.0);
}

float rand(vec2 co)
{
    return fract(sin(dot(co.xy , vec2(12.9898, 78.233))) * 43758.5453);
}

vec4 lv4(float t) {
    float sizeDelta = 5.0;
    float size = 20.0 + t * sizeDelta;
    float prob = 0.99;
    
    vec2 pos = floor(1.0 / size * gl_FragCoord.xy);
    
    float color = 0.0;
    float starValue = rand(pos);
    
    if (starValue > prob)
    {
        vec2 center = size * pos + vec2(size, size) * 0.5;
        
        float ti = 0.9 + 0.2 * sin(t + (starValue - prob) / (1.0 - prob) * 45.0);
        
        color = 1.0 - distance(gl_FragCoord.xy, center) / (0.5 * size);
        color = color * ti / (abs(gl_FragCoord.y - center.y)) * ti / (abs(gl_FragCoord.x - center.x));
    }
    else if (rand(gl_FragCoord.xy / u_resolution.xy) > 0.996)
    {
        float r = rand(gl_FragCoord.xy);
        color = r * (0.25 * sin(t * (r * 5.0) + 720.0 * r) + 0.75);
    }
    
    vec3 color_a = vec3(0.0471, 0.0471, 0.1176);
    vec3 color_b = vec3(0.0706, 0.0, 0.2314);
    vec3 bg_color = mix(color_b, color_a, gl_FragCoord.y / u_resolution.y);
    
    vec3 pix_color = bg_color + vec3(color);
    
    return vec4(pix_color, 1.0);
}

void main() {
    if (level == 0) {
        frag_color = lv0(u_time);
    } else if (level == 1) {
        frag_color = lv1(u_time);
    } else if (level == 2) {
        frag_color = lv2(u_time);
    } else if (level == 3) {
        frag_color = lv3(u_time);
    } else if (level == 4) {
        frag_color = lv4(u_time * 0.01);
    } else {
        frag_color = vec4(0.9, 0.9, 0.9, 1.0);
    }
}
