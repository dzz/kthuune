#version 330

uniform float tick;
uniform float impulse;
uniform sampler2D texBuffer;
uniform float statusamt;
uniform vec4 statuscolor;
in vec2 uv;

void main(void) {
    vec4 smpl_base = texture(texBuffer,uv);
    smpl_base.rgb = smpl_base.rgb * statuscolor.rgb * ((0.7*(1.0-uv.y))+0.3);

    float challenge = uv.x + ((sin( (uv.y*16) + (tick*(1.0+uv.x)) )*0.03)*cos(tick*1.3));

    if( challenge>statusamt) {
        smpl_base.rgb*=0.5*uv.x;
    }

    smpl_base.a *= impulse;
    smpl_base.rgb *= (1.0-uv.y);
    gl_FragColor = smpl_base;
}

