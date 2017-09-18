#version 330

uniform vec4 filter_color;
uniform sampler2D texBuffer;
in vec2 uv;


void main(void) {
    
    float grad = 0.8 + (uv.y*0.2);
    vec4 smpl_base = texture(texBuffer,uv);
    gl_FragColor = smpl_base * filter_color * grad;
}

