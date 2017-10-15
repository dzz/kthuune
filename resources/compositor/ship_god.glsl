#version 330

in vec2 uv;
uniform float amt;
uniform sampler2D scene;

void main() {

    vec4 base = texture( scene, uv);

    float l = length(base);

    float ql = smoothstep(0.0,1.0,l*l*l);
    vec4 color = base;

   
    color.r = color.r*l;
    color.g = color.g*ql;
    color.b = color.b+(ql*0.5);

    float nl = length(color.rgb);

    color.r*=nl;
    color.g*=nl;
    color.b*=nl;
    gl_FragColor = (color*ql)+(base*(1.0-l));
    
}
