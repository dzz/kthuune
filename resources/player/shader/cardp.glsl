#version 330

uniform float tick;
uniform sampler2D texBuffer;
uniform float statusamt;
uniform vec4 statuscolor;
in vec2 uv;

#define NUM_OCTAVES 8

float random (in vec2 _st) {
    return fract(sin(dot(_st.xy,
                         vec2(12.9898,78.233)))*
        43758.5453123);
}
// Based on Morgan McGuire @morgan3d
// https://www.shadertoy.com/view/4dS3Wd
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

vec4 clouds(vec2 _coord) {

    float ti = tick*0.1;
    vec2 coord = _coord;
    coord.x -= 0.5;
    coord.y -= 0.5;

    float u_time = tick/5.0;

    vec2 st = coord*4+((vec2(0.1,-0.1)));
    //st += st * abs(sin(u_time*0.1)*3.0);
    vec3 color = vec3(0.0);

    vec2 q = vec2(0.);
    q.x = fbm( st + 0.00*u_time);
    q.y = fbm( st + vec2(1.0));

    vec2 r = vec2(0.);
    r.x = fbm( st + 1.0*q + vec2(1.7,9.2)+ 0.15*u_time );
    r.y = fbm( st + 1.0*q + vec2(8.3,2.8)+ 0.126*u_time);

    float f = fbm(st+r);


    f = f+0.25;
    color = mix(vec3(0.6,0.3,0.9),
                vec3(1.0,0.0,1.0),
                clamp((f*f)*4.0,0.0,1.0));

    color = mix(color,
                vec3(0.7,0.4,0.9),
                clamp(length(q),1.0,1.0));

    color = mix(color,
                vec3(0.7,0.5,1),
                clamp(length(r.x),0.0,1.0));

    vec4 ret = vec4((f*f*f+.6*f*f+.5*f)*color,1.);
    return ret*ret;
}

void main(void) {
    vec4 smpl_base = texture(texBuffer,uv);

    if(smpl_base.r<0.5) {
            smpl_base = clouds(uv + vec2(tick*0.02,-(0.1*tick*2)));
            smpl_base.g = 0.5;
        }
    else {
        float idx = 1.0 - uv.y;

        if(idx<statusamt) {
            smpl_base = idx * statuscolor;
        } else {
            smpl_base = (vec4(1.0,1.0,1.0,1.0)-statuscolor)*(1.0-idx);
        }
    }
        //smpl_base = vec4(1.0,1.0,1.0,1.0) - clouds(uv - vec2(tick*0.2,-0.1*tick*2));

    smpl_base.a = 1.0;
    gl_FragColor = smpl_base;
}

