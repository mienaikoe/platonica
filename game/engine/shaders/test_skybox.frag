#ifdef GL_ES
precision mediump float;
#endif

uniform float u_time;
uniform vec2 u_resolution;

float dist(vec2 p0, vec2 pf) {
    return sqrt((pf.x - p0.x) * (pf.x - p0.x) + (pf.y - p0.y) * (pf.y - p0.y));
}

float clamp_normal(float i) {
    return clamp(i, 0.0, 1.0);
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
/*
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
*/

// float rand(float co) { return fract(sin(co*(91.3458)) * 47453.5453); }

vec4 lv2(float t){
    vec3 base_color = vec3(0.8, 0.9333, 0.8863);
    vec3 effect_color = vec3(0.8667, 0.9686, 0.9608);
    
    vec2 uv = gl_FragCoord.xy / u_resolution.xy;
    float curve = -0.1 * tan((t * uv.y) + (3.0 * uv.x));
    float d = clamp_normal(distance(curve + uv.y, 0.5));
    float line_shape = smoothstep(1.0 - d, 1.0, 0.95);
    vec3 line_color = vec3(mix(effect_color, base_color, line_shape));
    
    return vec4(line_color, 1.0);
}
/*
vec4 lv3(float t) {
    vec2 center = vec2(0.1, 0.1); // TODO pass in random position
    
    float speed = 0.01;
    
    float aspect_ratio = u_resolution.y / u_resolution.x;
    
    vec2 uv = gl_FragCoord.xy / u_resolution.xy;
    
    vec3 color = vec3(0.2431, 0.451, 0.6118);
    vec3 bg_color = vec3(0.2078, 0.2745, 0.4902);
    // vec4(uv, 0.5 + 0.5 * sin(t), 1.0).xyz;
    
    float x = (center.x - uv.x);
    float y = (center.y - uv.y) * aspect_ratio;
    
    //float r = -sqrt(x*x + y*y); //uncoment this line to symmetric ripples
    float r = - 0.5 * (x * x + y * y);
    float z = 0.3 * sin((r + t * speed) / 0.02);
    
    vec3 ripple_color = mix(bg_color, color, clamp(z, 0.0, 1.0));
    
    return vec4(ripple_color, 1.0);
}
*/

void main() {
    gl_FragColor = lv2(mod(u_time, 6.28) - 3.14);
}
