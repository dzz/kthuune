#version 330


in vec2 uv;
uniform float amt;
uniform sampler2D scene;

// @load "includes/colors.glsl"

void main() {

    vec4 base = texture( scene, uv);

    float l = length(base.rgb);

    l-=0.5;
    l*=2.0;
    l*=l;

    l+=1.8;
    l=smoothstep(l,0.0,1.0);

    vec3 photo = vec3(l*base.r,l*base.g,l*base.b);
    //vec3 hsl_base = rgb2hsv(base.rgb);
    vec3 hsl_photo = rgb2hsv(photo);


   // gl_FragColor.rgb= vec3(l,l,l);

    vec3 uv_fix = photo*vec3(1.0,0.9,0.4);
    gl_FragColor.rgb= (uv_fix*(hsl_photo.y))+(photo*(1.0-hsl_photo.y));
    gl_FragColor.a = 1.0;
}
