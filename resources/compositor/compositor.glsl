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

    return sampled/4;
}

void main(void) {

    vec2 centered_uv = (uv+vec2(-0.5,-0.5))*2;
    centered_uv*= centered_uv;


    vec4 height_texel = cheap_blur(uv, height_buffer, 1.0/120 );

    float parallax_ratio = 0.01+ (0.08 * height_texel.r);
    float from_c = length(centered_uv);

    vec2 parallaxed_uv = ((uv-vec2(0.5,0.5)) * (1.0+(parallax_ratio * from_c ))) + vec2(0.5,0.5);
    

    vec4 photon_texel =  cheap_blur(uv, photon_buffer, 1.0/640);
    vec4 floor_texel = texture(floor_buffer,parallaxed_uv);
    vec4 light_texel = cheap_blur( uv, light_buffer, 1.0/60);
    vec4 object_texel = texture( object_buffer, parallaxed_uv );
    //vec4 object_texel = cheap_blur( parallaxed_uv, object_buffer, 1.0/320.0 );
    vec4 vision_texel = cheap_blur( parallaxed_uv, vision_buffer, 1.0/160.0 );



    //vec4 reflect_texel = texture(reflect_buffer, parallaxed_uv );
    //vec4 reflect_map_texel = texture(reflect_map, (orient + par_mod) - (height_mod*2));
    //vec2 base_reflect_parallaxed_uv = (orient + par_mod) - (height_mod*2);
    //vec4 reflect_map_texel = cheap_blur( base_reflect_parallaxed_uv*0.25, reflect_map, 1.0/256 );


    float exposure = 1.8;
    float ambiance = 0.2;

    vec4 LitObject = object_texel * (light_texel * exposure);
    vec4 LitFloor = ( (photon_texel * floor_texel * light_texel) * exposure) + (ambiance*photon_texel);

    float mask = 1.0 - LitObject.a;
    vec4 SeenFloor = (LitFloor * vision_texel) * mask;

    LitObject = LitObject * LitObject.a;

    gl_FragColor = SeenFloor + LitObject;

}

