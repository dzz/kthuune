#version 330


in vec2 uv;
uniform float amt;
uniform float g;
uniform float b;
uniform float s;
uniform float t;
uniform float tick;
uniform sampler2D scene;

// @load "includes/colors.glsl"

void main() {

    vec2 c_uv = vec2(0.5,0.5) - uv;
    float d = ((1.0-t)*length(c_uv))*0.3;

    vec4 centerc = texture( scene, uv );
    float divergence = 0.005 + (0.005*length(centerc))*(0.2+(t*0.8)+(g*0.4)+(b*3.2))*0.2;

    divergence *= (30*t);

    vec2 r_offs = vec2(0.0,-divergence) * d;
    vec2 g_offs = vec2(-divergence,divergence) * d;
    vec2 b_offs = vec2(divergence,divergence) * d;

    vec4 base_r = texture( scene, uv+r_offs);
    vec4 base_g = texture( scene, uv+g_offs);
    vec4 base_b = texture( scene, uv+b_offs);

    vec4 base = vec4( base_r.r, base_g.g, base_b.b, 1.0 );


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


    float mg=g*((sin(tick*0.01)+1.0)/2.0);
    gl_FragColor.rgb = (comp*(1.0-mg))+(inv*mg);
    gl_FragColor.rgb*=vec3(1.0,1.0,1.0)+vec3(b*45,b*40,b*30);

    gl_FragColor.rgb = ((1.0-s)*gl_FragColor.rgb)+(s*vec3(comp.r,1.0-l,1.0-l));

    gl_FragColor.rgb*= (1.0-t);

    gl_FragColor.rgb+=t*vec3(1.0-l,1.0-l,1.0-l);
    gl_FragColor.a = 1.0;
}
