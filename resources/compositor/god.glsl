#version 330

in vec2 uv;
uniform float amt;
uniform sampler2D scene;

void main() {
    vec4 base = texture( scene, uv );

    float l = length(base);

    l = smoothstep(0.0,1.0,l*l*l*l*l);
    vec4 color = base;

    color.r=base.b;
    color.g=base.r;
    color.b=base.g;

    
    gl_FragColor = base;

    
}
