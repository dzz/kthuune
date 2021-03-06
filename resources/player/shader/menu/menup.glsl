#version 330

uniform sampler2D texBuffer;
uniform float tick;
uniform float alpha;
in vec2 uv;


void main(void) {

    float final_alpha = alpha;
    vec2 frq = uv.xy * vec2(30,40);
    vec2 offs = (vec2(sin(tick+frq.x),cos(tick+frq.y))*0.01)*uv.y*2;

    if(offs.x>0)
        offs.y=0;
    

    vec2 uv2 = uv;
    uv2 -= vec2(0.5,0.5);
    uv2 *= 0.5 + (alpha*0.5);

    uv2 += vec2(0.5,0.5);
 
    vec4 smpl_base = texture(texBuffer,uv2+offs);
    vec4 shadow_base = texture(texBuffer,uv2+offs+vec2(0.0,-0.01));

    int si = int(floor(uv.y*900));

    float l=length(uv-vec2(0.5,0.5));
    if(smpl_base.r <1.0) {

        int ii = int(uv.x*1920)%32;
        int jj = int(uv.y*1080)%32;

        if(ii<9) {
            smpl_base = vec4(0.0,0.0,0.0,1.0);
        } else
        if(jj<9) {
            smpl_base = vec4(0.0,0.0,0.0,1.0);
        } else
        if(shadow_base.r>0.9) {
            smpl_base = vec4(0.0,0.15,0.0,1.0);
        } else
        /*if(si%2==0)
            smpl_base = vec4(0.0,0.0,0.0,1.0);
        else */{
            int check = int(sin((uv.x+cos(tick))*20)*sin(tick)*20*l);
            int modv = (check%10)-5;
            float modp = modv/10.0f;
            float idx1 = (1.0+sin((uv.y*6)+(tick*3.0)+(modp*3.14)))/2.0;
            smpl_base = vec4(0.1*idx1,0.0,idx1*0.3,1.0);
        }


        final_alpha *= final_alpha;
        final_alpha *= final_alpha;
    } else {
        float idx1,idx2;
        //if(si%2==1) {
            idx1 = abs(sin(((uv.y*45*(1.0-l))+(tick*2))));
            idx2 = abs(sin(((uv.y*25*(1.0-l))+(tick*3))));
        //} /*else */{
        //    idx1 = 0.0;
        //    idx2 = 0.2;
        //}*/
        smpl_base = (vec4( 1.0,1.0,0.0,1.0)*idx1)+(vec4(1.0,1.0,1.0,1.0)*(1.0-idx1));

        smpl_base = (smpl_base*idx2)+vec4(0.0,1.0,1.0,1.0)*(1.0-cos(idx1));
        final_alpha *= 2.0; 
    }


    if(final_alpha>1.0) final_alpha = 1.0;

    gl_FragColor = smpl_base;
    gl_FragColor.a = final_alpha;

}
