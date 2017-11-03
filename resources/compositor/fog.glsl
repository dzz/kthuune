#version 330

// @load "includes/uvs.glsl"

in vec2 uv;
uniform float parallax;
uniform float fog_level;
uniform vec2 camera_position;
uniform sampler2D light_buffer;
uniform sampler2D vision_tex;
uniform float tick;

float random (in vec2 _st) {
    return fract(sin(dot(_st.xy,
                         vec2(12.9898,78.233)))*
        43758.5453123);
}
float noise (in vec2 _st) {
    vec2 i = floor(_st);
    vec2 f = fract(_st);

    // Four corners in 2D of a tile
    float a = random(i);
    float b = random(i + vec2(1.0, 0.0));
    float c = random(i + vec2(0.0, 1.0));
    float d = random(i + vec2(1.0, 1.0));

    vec2 u = f * f * (3.0 - 2.0 * f);

    return mix(a, b, u.x) +
            (c - a)* u.y * (1.0 - u.x) +
            (d - b) * u.x * u.y;
}
#define NUM_OCTAVES 4

float fbm ( in vec2 _st) {
    float v = 0.0;
    float a = 0.5;
    vec2 shift = vec2(100.0);
    // Rotate to reduce axial bias
    mat2 rot = mat2(cos(0.5), sin(0.5),
                    -sin(0.5), cos(0.50));
    for (int i = 0; i < NUM_OCTAVES; ++i) {
        v += a * noise(_st);
        _st = rot * _st * 2.0 + shift;
        a *= 0.5;
    }
    return v;
}
vec4 clouds(vec2 _coord, float l) {

    float ti = tick*0.1;
    vec4 tcol = texture(light_buffer,_coord);
    vec2 coord = _coord;
    coord.x -= 0.5;
    coord.y -= 0.5;

    float damt = length(coord)*2.1*length(tcol);

    //coord*=(1.0+(damt*2));

    float u_time = tick/65.0;

    u_time -= (l*1.2*parallax);

    vec2 st = coord*4+(camera_position*(vec2(0.1,-0.1)));
    //st += st * abs(sin(u_time*0.1)*3.0);
    vec3 color = vec3(0.0);

    vec2 q = vec2(0.);
    q.x = fbm( st + 0.00*u_time);
    q.y = fbm( st + vec2(1.0));

    vec2 r = vec2(0.);
    r.x = fbm( st + 1.0*q + vec2(1.7,9.2)+ 0.15*u_time );
    r.y = fbm( st + 1.0*q + vec2(8.3,2.8)+ 0.126*u_time);

    float f = fbm(st+r);

    color = mix(vec3(0.7,0.8,0.9),
                vec3(1.0,1.0,1.0),
                clamp((f*f)*4.0,0.0,1.0));

    color = mix(color,
                vec3(0.8,0.7,0.9),
                clamp(length(q),1.0,1.0));

    color = mix(color,
                vec3(1.0,1,1),
                clamp(length(r.x),0.0,1.0));

    vec4 ret = vec4((f*f*f+.6*f*f+.5*f)*color,1.);
    return ret*ret;
}

vec2 shift(vec2 v) {
    return vec2(v.x-0.5,v.y-0.5);
}

vec2 unshift(vec2 v) {
    return vec2(v.x+0.5,1.0-(v.y+0.5)) ;
}

void main(void) {

    //float parallax = 0.01;
    vec2 scp = (camera_position*vec2(1.0,-1.0)) * parallax;
    float l = 2.0 - length(shift(uv));
    float warp = 0.25+(0.8*l);
    vec2 shifted = shift(uv + scp)*-1*warp;
    
    vec2 floor_uv = get_floor_uv(uv);
    vec4 vision_texel = texture( vision_tex, floor_uv);

    vec2 light_uv = get_parallax_uv(uv);

    vec4 light_texel = texture( light_buffer, light_uv) * smoothstep(0.0,1.0,vision_texel*24);


    vec2 cloud_uv = get_fisheye_uv( uv, 0.9,2.5);
    vec2 icloud_uv = get_fisheye_uv( uv, 1.2,3.0);
    vec4 base = (clouds( cloud_uv, l ) + clouds(icloud_uv, l))/2;

    vec4 computed = base;

    computed.a = 0.5+(computed.r*0.5);

    computed.a = computed.a * (1.0-vision_texel.r);
    

    computed.rgb *= vec3(0.6,0.5,0.8)+light_texel.rgb;
    
        //computed.r *= (1.0 - vision_texel.r);
        //computed.g *= (1.0 - vision_texel.r);
        //computed.b *= (1.0 - vision_texel.r);

    computed.a = computed.a * smoothstep(0.0,0.9,(fog_level*fog_level)*2.7);
    gl_FragColor = computed;
    //gl_FragColor = clouds(uv*parallax*warp);
}
