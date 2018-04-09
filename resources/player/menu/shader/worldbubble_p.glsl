#version 330

// @description: passes through texture pixels, tints by a filter_color

uniform sampler2D texBuffer;
uniform vec4 filter_color;
in vec2 uv;

void main(void) {
    vec4 smpl_base = texture(texBuffer,uv);
    //vec4 smpl_base = vec4( 1.0,0.0,1.0,1.0 );
    gl_FragColor = smpl_base;
}


