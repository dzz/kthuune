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

    float l=length(uv-vec2(0.5,0.5));
    if(smpl_base.r <1.0) {

        int check = int(sin((uv.x+cos(tick))*20)*sin(tick)*20*l);
        int modv = (check%10)-5;
        float modp = modv/10.0f;
        float idx1 = (1.0+sin((uv.y*6)+(tick*3.0)+(modp*3.14)))/2.0;
        smpl_base = vec4(0.1*idx1,0.0,idx1*0.3,1.0);
    } else {
        float idx1 = abs(sin(((uv.y*45*(1.0-l))+(tick*2))));
        float idx2 = abs(sin(((uv.y*25*(1.0-l))+(tick*3))));
        smpl_base = (vec4( 1.0,1.0,0.0,1.0)*idx1)+(vec4(1.0,1.0,1.0,1.0)*(1.0-idx1));

        smpl_base = (smpl_base*idx2)+vec4(0.0,1.0,1.0,1.0)*(1.0-cos(idx1));
    }

    gl_FragColor = smpl_base;

}
