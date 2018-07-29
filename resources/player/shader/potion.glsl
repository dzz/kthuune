#version 330

uniform float tick;
uniform sampler2D texBuffer;
uniform float statusamt;
uniform vec4 statuscolor;
uniform float flashamt;
in vec2 uv;


bool shade_blue() {

    float waveamt = sin(tick*3.0);
    float intercept = uv.y;
    float waveval = cos((tick+uv.x)*12.0+(8.0*flashamt))*waveamt;

    waveval*= 0.01;

    intercept+=waveval;

    if(intercept > (1.0-statusamt) ) 
        return true;

}

void main(void) {
    vec4 smpl_base = texture(texBuffer,uv);
    gl_FragColor = smpl_base;
//
//    vec4 smpl_base = texture(texBuffer,uv)* ((0.5)+(uv.y*0.5));
//
//    vec3 flash_color = vec3(1.0,1.0,1.0)*flashamt;
//
//    //if(uv.y > (1.0-statusamt) ) {
//    if( shade_blue() ) {
//        smpl_base.rgb *= vec3(1.0,1.0,1.0) + (flash_color*uv.y);
//    }
//
//    smpl_base.rgb += (flash_color*(1.0-uv.y));
//
//    gl_FragColor = smpl_base;
}

