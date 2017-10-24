#version 330

in vec2 uv;
uniform float amt;
uniform sampler2D scene;

void main() {

    float eps = 0.001;

    float le = length(uv-vec2(0.5,0.5));

    eps *= (1.0)+le;
    vec4 base = texture( scene, uv+vec2(0.0,-eps));
    vec4 base2 = texture( scene, uv+vec2(eps,eps));
    vec4 base3 = texture( scene, uv+vec2(-eps,eps));


    float sl = (1.0+(sin(uv.y*720*3.14)))/2.0;
    float l = max(base.r,base.g);
    l = max(l,base.b);
    l=smoothstep(0.0,1.0,l*l*1.4);

    float l2 = max(base2.g,base2.b);
    l2 = max(l2,base2.r);
    l2=smoothstep(0.0,1.0,l2*l2*1.4);

    float l3 = max(base3.b,base3.r);
    l3 = max(l3,base3.g);
    l3=smoothstep(0.0,1.0,l3*l3*1.4);

    //if(l<0.5) l*=0.8; else l*=1.2;

    //vec4 gray = vec4(l,l,l,1.0);

    //gray.rgb*=0.5;
    //gray.rgb+=base.rgb*0.5;

    //base.gb*=l;
    //gl_FragColor = vec4(l,l2,l3,0)*sl;
    
    gl_FragColor = vec4( base.r, base2.g, base3.b, 1.0);
    
}
