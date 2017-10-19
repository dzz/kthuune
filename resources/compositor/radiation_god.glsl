#version 330

in vec2 uv;
uniform float amt;
uniform sampler2D scene;

void main() {

    vec4 base = texture( scene, uv);


    float l = max(base.r,base.g);
    l = max(l,base.b);

    l=smoothstep(0.0,1.0,l*l*1.7);


    if(l<0.5) l*=0.8; else l*=1.2;

    gl_FragColor = vec4(l,l,l,1.0);
    
}
