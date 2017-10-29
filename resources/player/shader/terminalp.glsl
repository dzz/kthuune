#version 330

uniform float tick;
uniform sampler2D texBuffer;
uniform vec4 filter_color;
in vec2 uv;

// @load "../../compositor/includes/noise.glsl"

void main(void) {
    vec4 smpl_base = texture(texBuffer,uv);

    float l = length(uv-vec2(0.5,0.5));
    float d_amt = l*cos(uv.y+tick*0.01);
    vec2 noisey_offset = vec2( random(uv*1000+tick), random(uv*-3000+tick))*(d_amt*d_amt*d_amt*0.03)*sin(uv.y+(tick*0.01)*600);

    if((smpl_base.r+smpl_base.g+smpl_base.g)==0)
        gl_FragColor = smpl_base*(1.0-l);
    else
        gl_FragColor = texture(texBuffer, uv+noisey_offset)*(0.7+(l*0.3));

    gl_FragColor.rgb *= vec3(1.0,0.8,0.2);

}
