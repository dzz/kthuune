#version 330

// @load "includes/uvs.glsl"

in vec2 uv;
uniform float parallax;
uniform float fog_level;
uniform vec2 camera_position;
uniform sampler2D bg_texture;
uniform sampler2D vision_tex;

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
    vec2 shifted = shift(get_floor_uv(uv) + scp)*warp;

    vec4 vision_texel = texture( vision_tex, get_floor_uv(uv) );
    vision_texel.a = 1.0;

    vec4 texel = texture( bg_texture, unshift(shifted*0.2) );


    texel.rgb *= smoothstep(0.0,1.0,vision_texel.r*7);
    gl_FragColor = texel;
}
