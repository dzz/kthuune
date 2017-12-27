#version 330

in vec2 uv;
uniform float open_amt;
uniform sampler2D menu;

void main() {
    gl_FragColor = texture( menu, uv )*open_amt;
}
