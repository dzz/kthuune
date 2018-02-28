#version 330

uniform sampler2D texBuffer;
uniform float tick;
in vec2 uv;


void main(void) {

    vec2 frq = uv.xy * vec2(30,40);

    vec2 offs = (vec2(sin(tick+frq.x),cos(tick+frq.y))*0.01)*uv.y*2;

    if(offs.x>0)
        offs.y=0;
    

    vec4 smpl_base = texture(texBuffer,uv+offs);

    if(smpl_base.r <1.0) {

        vec2 tuv = uv + (vec2(sin(tick*0.1),cos(tick*0.3))*2.0);
        vec2 frq = vec2(tuv.x*20,tuv.y*20);

        frq*=length(uv-vec2(0.5,0.5));
        float a = sin( frq.x );
        float b = cos( frq.y );

        if(a>0)
            a = 1.0;
        else 
            a = 0.0;
        if(b>0)
            b = 0.0;
        else 
            b = 1.0;

        frq*=0.4;
        float idx1 = ( (a*b)+cos(frq.x+tick)+sin(frq.y+tick) );


        if(idx1<0)
            idx1 = 1.0 + idx1;
        smpl_base = vec4(0.3*a,0.2*b,idx1*0.7,1.0);
    } else {
        float idx1 = sin(uv.y*(20*uv.y)+(tick*uv.y));
        smpl_base = vec4( idx1,idx1,0.0,1.0);
    }

    gl_FragColor = smpl_base;

}
