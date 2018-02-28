#version 330 core


in vec2 input_position;
in vec2 uv_position;

out vec2 uv;

void main(void) {

    uv=uv_position;
    uv.y = 1.0 - uv.y;
    gl_Position.xy = input_position;
    gl_Position.z = 0;
    gl_Position.w = 1;
}

