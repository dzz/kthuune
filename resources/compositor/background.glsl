#version 330

in vec2 uv;
uniform float parallax;
uniform vec2 camera_position;
uniform sampler2D vision_tex;
uniform sampler2D bg_texture;

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
    vec2 shifted = shift(uv + scp)*warp;

    vec4 vision_texel = texture( vision_tex, uv );
    vision_texel.a = 1.0;

    vision_texel = smoothstep(0.0,1.0, vision_texel*24);
    
    vec4 texel = texture( bg_texture, unshift(shifted*0.2) ) * vision_texel;
    gl_FragColor = texel;
}
