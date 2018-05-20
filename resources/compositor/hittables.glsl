
#version 330

in vec2 uv;
uniform float amt;
uniform sampler2D hittables;

vec2 scaleup( vec2 o, float scl ) {

    o -= vec2(0.5,0.5);
    o*=scl;

    o +=vec2(0.5,0.5);

    return o;
}
void main() {

    float modamt = (amt*amt*amt);
    vec4 samp = (
        texture( hittables, scaleup(uv,0.9)) +
        texture( hittables, scaleup(uv,0.8)) +
        texture( hittables, scaleup(uv,0.6))
        )/3.0;

    float famt = samp.a;

    gl_FragColor = vec4( 1.0,0.8,0.5,1.0) * famt * modamt * 0.25;
    //gl_FragColor = vec4( halo.r,samp.g, samp.b, 1.0) * famt * amt;
}
