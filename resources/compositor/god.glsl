#version 330

in vec2 uv;
uniform float amt;
uniform sampler2D scene;

void main() {
    vec4 base = texture( scene, uv );

    gl_FragColor = base*length(base*base);
}
