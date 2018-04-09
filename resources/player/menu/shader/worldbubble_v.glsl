
#version 330 core

// @description: transforms a unit square into a location within a view

uniform vec2 view;
uniform vec2 scale_local;
uniform vec2 scale_world;
uniform float scale_x;
uniform vec2 translation_local;
uniform vec2 translation_world;
uniform float rotation_local;

in vec2 input_position;
in vec2 uv_position;

out vec2 uv;

void main(void) {
    
    
    gl_Position.xy = (input_position.xy*vec2(0.5*scale_x,0.66)) + vec2( 0.5,0.0);
    gl_Position.zw = vec2(0,1);
    uv=uv_position;
    uv.y = 1.0 - uv.y;
    //gl_Position.x *= scale_x;
        
}

