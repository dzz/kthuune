#version 330

in vec2 uv;
uniform sampler2D canopy_buffer;
uniform sampler2D light_buffer;

void main() {
    vec4 samp = texture( canopy_buffer, uv );
    vec4 light = texture( light_buffer, uv );


    light = light*light*1.7;
    light = light+vec4(1.0,1.0,1.0,1.0);
    light/=2;

    vec4 lit = samp*light;

    lit.a = samp.a;
    
    gl_FragColor = samp * light;
}
