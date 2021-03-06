#version 330 core

// @description: transforms a unit square into a location within a view

uniform float tick;
uniform vec2 view;
uniform vec2 scale_local;
uniform vec2 scale_world;
uniform vec2 translation_local;
uniform vec2 translation_world;
uniform float rotation_local;
uniform float impulse;

in vec2 input_position;
in vec2 uv_position;

out vec2 uv;

void main(void) {
    
    float amp = 1.0+(impulse * 0.15);
    float x = ((input_position.x+translation_local.x)*scale_local.x)*amp;
    float y = ((input_position.y+translation_local.y)*scale_local.y)*amp;

    float xt = x * cos(rotation_local)  - y * sin(rotation_local);
    float yt = x * sin(rotation_local)  + y * cos(rotation_local);

    gl_Position.x =  ((xt)+translation_world.x) * scale_world.x * view.x;
    gl_Position.y =  ((yt)+translation_world.y) * scale_world.y * view.y;
    gl_Position.z = 0;
    gl_Position.w = 1;

    uv=uv_position;
        
}

