
#version 330

in vec2 uv;
uniform float amt;
uniform sampler2D hittables;

void main() {

    vec4 samp = texture( hittables, uv);

    float famt = samp.a;

    gl_FragColor = vec4( 1.0,0.8,0.5,1.0) * famt * amt;
    //gl_FragColor = vec4( halo.r,samp.g, samp.b, 1.0) * famt * amt;
}
