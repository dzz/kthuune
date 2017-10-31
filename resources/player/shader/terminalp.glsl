#version 330

uniform float tick;
uniform float size;
uniform sampler2D texBuffer;
uniform vec4 filter_color;
in vec2 uv;


void main(void) {
    vec4 smpl_base = texture(texBuffer,uv);


    float scanline = 0.75 + (abs(sin(uv.y*400+tick))*0.25);
    float l = uv.y;
    if((smpl_base.r+smpl_base.g+smpl_base.g)==0)
        gl_FragColor = (1.2-l)*vec4(0.3,0.5,0.8,0.5)*scanline;
    else
        gl_FragColor = smpl_base;

    gl_FragColor.rgba*= size;
    gl_FragColor.rgba+= (vec4(1.0,1.0,1.0,1.0)*(1.0-size));
    //gl_FragColor.rgb *= vec3(1.0,0.8,0.2);

}
