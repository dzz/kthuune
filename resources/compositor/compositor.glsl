#version 330

// @description: composite the floor together

uniform vec2 camera_position;

uniform sampler2D floor_buffer;
uniform sampler2D light_buffer;
uniform sampler2D object_buffer;
uniform sampler2D vision_buffer;
uniform sampler2D photon_buffer;
uniform sampler2D height_buffer;
uniform sampler2D reflect_buffer;
uniform sampler2D reflect_map;
in vec2 uv;

vec4 cheap_blur( vec2 p_uv, sampler2D p_buffer, float p_size ) {

    float lmod = 1;
    vec4 sampled = texture( p_buffer, p_uv + lmod*vec2( p_size, 0.0 ) ) +
                    texture( p_buffer, p_uv + lmod*vec2( -1*p_size, 0.0 ) ) +
                    texture( p_buffer, p_uv + lmod*vec2( 0.0, p_size ) ) +
                    texture( p_buffer, p_uv + lmod*vec2( 0.0, -1*p_size ) );

    return (sampled * sampled)*0.07;
}

void main(void) {

    vec2 centered_uv = (uv+vec2(-0.5,-0.5))*2;
    centered_uv*= centered_uv;

    vec2 par_mod = camera_position * 0.3 * vec2(1.0,-1.0)*0.15;

    vec4 height_texel = texture(height_buffer, uv);
    
    vec2 orient = vec2( sin( centered_uv.x*3.14),cos(centered_uv.y*3.14) ) * 0.05;
    vec2 height_mod = height_texel.r * orient * 0.1;

    vec4 photon_texel =  cheap_blur(uv + (height_mod*5), photon_buffer, 1.0/640) * (height_texel.r*0.5);
    vec4 floor_texel = texture(floor_buffer,uv + height_mod*0.5);
    vec4 light_texel = cheap_blur( uv + height_mod , light_buffer, 0.1);
    vec4 object_texel = cheap_blur( uv, object_buffer, 1.0/320.0 );//texture(object_buffer, uv);
    vec4 vision_texel = cheap_blur( uv, vision_buffer, 1.0/160.0 );
    vec4 reflect_texel = texture(reflect_buffer, uv );
    
    //vec4 reflect_map_texel = texture(reflect_map, (orient + par_mod) - (height_mod*2));

    vec2 base_reflect_uv = (orient + par_mod) - (height_mod*2);
    vec4 reflect_map_texel = cheap_blur( base_reflect_uv*0.25, reflect_map, 1.0/256 );

    // these are just some basics, to be parameterized and tweaked in the future 


    //light_texel = ((light_texel*light_texel) + (photon_texel*photon_texel)/2.0);

    light_texel = photon_texel+light_texel;
    light_texel = light_texel * vision_texel;
    vec4 lit_floor = ((light_texel*floor_texel)*1.0)*(1.0-object_texel.a);
    vec4 lit_object = object_texel * photon_texel;

    float ooa = object_texel.a;

    vec4 lit_reflection = reflect_texel * light_texel * reflect_map_texel;

    lit_floor = lit_floor + lit_reflection;

    
    vec4 ot = object_texel + light_texel;
    gl_FragColor = ((lit_floor*light_texel)*(1.0-ooa)) + (vec4(ot.r*ooa,ot.g*ooa,ot.b*ooa, ooa));


//    gl_FragColor = (lit_floor*light_texel + lit_object);

}

