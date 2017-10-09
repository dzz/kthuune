#version 330

in vec2 uv;
uniform float amt;
uniform sampler2D scene;

void main() {

    vec4 base = texture( scene, uv);

    float l = length(base);

    l = smoothstep(0.0,1.0,l*l*l);
    vec4 color = base;


    gl_FragColor = l*color;
    
}
