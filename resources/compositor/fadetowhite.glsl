#version 330

in vec2 uv;
uniform float amt;
uniform vec3 color;

void main(void) {
        
    gl_FragColor.rgb = color;
    gl_FragColor.a = amt;
}
