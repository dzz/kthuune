#version 330

// @description: composite the floor together

uniform float tick;
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

//float rand(float n){return fract(sin(n) * 43758.5453123);}
//
//float noise(float p){
//	float fl = floor(p);
//  float fc = fract(p);
//	return mix(rand(fl), rand(fl + 1.0), fc);
//}
	

vec4 cheap_blur( vec2 p_uv, sampler2D p_buffer, float p_size ) {


    float lmod = 1;

    float P = p_size;
    vec4 sampled =  
                    texture( p_buffer, p_uv + lmod*vec2( P, 0.0 ) ) +
                    texture( p_buffer, p_uv + lmod*vec2( -P, 0.0 ) ) +
                    texture( p_buffer, p_uv + lmod*vec2( 0.0, P ) ) +
                    texture( p_buffer, p_uv + lmod*vec2( 0.0, -P ) ) +

                    0.5*texture( p_buffer, p_uv + lmod*vec2( -P, -P ) ) +
                    0.5*texture( p_buffer, p_uv + lmod*vec2( P, P ) ) +
                    0.5*texture( p_buffer, p_uv + lmod*vec2( -P, -P ) ) +
                    0.5*texture( p_buffer, p_uv + lmod*vec2( P, P ) );

    return sampled/6;
}

void main(void) {


    vec2 UV = vec2(0.1,0.1)+(uv*0.8);
    vec2 centered_UV = (UV+vec2(-0.5,-0.5))*2;
    centered_UV*= centered_UV;


    vec4 height_texel = cheap_blur(UV, height_buffer, 1.0/120 );

    float parallax_ratio = 0.1+ (0.1 * height_texel.r);
    float from_c = length(centered_UV);

    from_c = from_c*from_c;

    vec2 parallaxed_UV = ((UV-vec2(0.5,0.5)) * (1.0+(parallax_ratio * from_c ))) + vec2(0.5,0.5);
    

    vec4 photon_texel =  cheap_blur(UV, photon_buffer, (from_c)*(1.0/640));
    vec4 floor_texel = texture(floor_buffer,parallaxed_UV);
    vec4 light_texel = cheap_blur( UV, light_buffer, (from_c)*1.0/60);
    vec4 object_texel = texture( object_buffer, parallaxed_UV );
    //vec4 object_texel = cheap_blur( parallaxed_UV, object_buffer, 1.0/320.0 );
    vec4 vision_texel = cheap_blur( parallaxed_UV, vision_buffer, (from_c)*(1.0/160.0) );



    //vec4 reflect_texel = texture(reflect_buffer, parallaxed_UV );
    //vec4 reflect_map_texel = texture(reflect_map, (orient + par_mod) - (height_mod*2));
    //vec2 base_reflect_parallaxed_UV = (orient + par_mod) - (height_mod*2);
    //vec4 reflect_map_texel = cheap_blur( base_reflect_parallaxed_UV*0.25, reflect_map, 1.0/256 );


    float exposure = 2.1;
    float ambiance = 0.3;

    vec4 LitObject = object_texel * (light_texel * exposure);
    vec4 LitFloor = ( (photon_texel * floor_texel * light_texel) * exposure) + (ambiance*photon_texel);

    float mask = 1.0 - LitObject.a;
    vec4 SeenFloor = (LitFloor * vision_texel) * mask;

    LitObject = LitObject * LitObject.a;

    gl_FragColor = SeenFloor + LitObject;

}

