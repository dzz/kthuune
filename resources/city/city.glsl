#version 330

in vec2 uv;
uniform float offs;
uniform sampler2D texBuffer;

void main(void) {
    gl_FragColor = texture( texBuffer, vec2(uv.x+offs, 1.0-uv.y));
    //gl_FragColor = vec4(1.0,1.0,1.0,1.0) - gl_FragColor;
}
