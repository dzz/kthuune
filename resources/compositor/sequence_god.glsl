#version 330


in vec2 uv;
uniform float amt;
uniform float g;
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

    vec3 uv_fix = photo*vec3(1.3,1.1,0.8);

    vec3 comp = (uv_fix*(hsl_photo.y))+(photo*(1.0-hsl_photo.y));
    //vec3 inv = vec3(1.0,1.0,1.0)-(vec3(l*l,l*l,l*l)*2);

    vec3 inv = comp*vec3(10,5,2); 

    gl_FragColor.rgb = (comp*(1.0-g))+(inv*g);
    gl_FragColor.a = 1.0;
}
