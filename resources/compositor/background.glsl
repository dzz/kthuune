#version 330

in vec2 uv;
uniform vec2 camera_position;

uniform sampler2D bg_texture;

vec2 shift(vec2 v) {
    return vec2(v.x-0.5,v.y-0.5);
}

vec2 unshift(vec2 v) {
    return vec2(v.x+0.5,v.y+0.5);
}

void main(void) {

    float parallax = 0.01;
    vec2 scp = camera_position * parallax;
    float l = 2.0 - length(shift(uv));
    float warp = 0.7+(0.3*l);
    vec2 shifted = shift(uv + scp)*warp;
    
    vec4 texel = texture( bg_texture, unshift(shifted*0.8) );
    gl_FragColor = texel;
}
