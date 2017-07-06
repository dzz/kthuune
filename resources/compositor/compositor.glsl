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

// Author @patriciogv - 2015
// http://patriciogonzalezvivo.com

#ifdef GL_ES
precision mediump float;
#endif

//uniform vec2 u_resolution;
//uniform vec2 u_mouse;
//uniform float u_time;

float random (in vec2 _st) {
    return fract(sin(dot(_st.xy,
                         vec2(12.9898,78.233)))*
        43758.5453123);
}

// Based on Morgan McGuire @morgan3d
// https://www.shadertoy.com/view/4dS3Wd
float noise (in vec2 _st) {
    vec2 i = floor(_st);
    vec2 f = fract(_st);

    // Four corners in 2D of a tile
    float a = random(i);
    float b = random(i + vec2(1.0, 0.0));
    float c = random(i + vec2(0.0, 1.0));
    float d = random(i + vec2(1.0, 1.0));

    vec2 u = f * f * (3.0 - 2.0 * f);

    return mix(a, b, u.x) +
            (c - a)* u.y * (1.0 - u.x) +
            (d - b) * u.x * u.y;
}

#define NUM_OCTAVES 4

float fbm ( in vec2 _st) {
    float v = 0.0;
    float a = 0.5;
    vec2 shift = vec2(100.0);
    // Rotate to reduce axial bias
    mat2 rot = mat2(cos(0.5), sin(0.5),
                    -sin(0.5), cos(0.50));
    for (int i = 0; i < NUM_OCTAVES; ++i) {
        v += a * noise(_st);
        _st = rot * _st * 2.0 + shift;
        a *= 0.5;
    }
    return v;
}

vec4 clouds(vec2 coord) {

    float u_time = tick/65.0;

    vec2 st = coord*4+(camera_position*(vec2(0.1,-0.1)));
    //st += st * abs(sin(u_time*0.1)*3.0);
    vec3 color = vec3(0.0);

    vec2 q = vec2(0.);
    q.x = fbm( st + 0.00*u_time);
    q.y = fbm( st + vec2(1.0));

    vec2 r = vec2(0.);
    r.x = fbm( st + 1.0*q + vec2(1.7,9.2)+ 0.15*u_time );
    r.y = fbm( st + 1.0*q + vec2(8.3,2.8)+ 0.126*u_time);

    float f = fbm(st+r);

    color = mix(vec3(0.7,0.8,0.9),
                vec3(1.0,1.0,1.0),
                clamp((f*f)*4.0,0.0,1.0));

    color = mix(color,
                vec3(0.8,0.7,0.9),
                clamp(length(q),1.0,1.0));

    color = mix(color,
                vec3(1.0,1,1),
                clamp(length(r.x),0.0,1.0));

    vec4 ret = vec4((f*f*f+.6*f*f+.5*f)*color,1.);
    return ret*ret;
}


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

    vec2 inv_UV = UV;
    float x_scale = 0.8+(0.6*(UV.y*UV.y));
    UV.x -= 0.5;
    UV.x *= x_scale;
    UV.x += 0.5;
    inv_UV.x -= 0.5;
    inv_UV.x *= 2.0-x_scale;
    inv_UV.x += 0.5;

    vec2 centered_UV = (UV+vec2(-0.5,-0.5))*2;
    centered_UV*= centered_UV;



    vec4 height_texel = cheap_blur(UV, height_buffer, 1.0/120 );


    float from_c = (length(centered_UV * vec2(1.7,1.0)))*1.2;
    
    float parallax_ratio = 0.1+ (0.1 * height_texel.r )*from_c;

    from_c = from_c*from_c;

    vec2 parallaxed_UV = ((UV-vec2(0.5,0.5)) * (1.0+(parallax_ratio * from_c ))) + vec2(0.5,0.5);
    vec2 inv_parallaxed_UV = ((inv_UV-vec2(0.5,0.5)) * (1.0+(parallax_ratio * (2.0-from_c) ))) + vec2(0.5,0.5);



    vec4 photon_texel =  cheap_blur(UV, photon_buffer, (from_c)*(1.0/32));
    vec4 floor_texel = texture(floor_buffer,parallaxed_UV);
    vec4 light_texel = cheap_blur( UV, light_buffer, (from_c)*1.0/60);
    vec4 object_texel = texture( object_buffer, inv_parallaxed_UV);
    //vec4 object_texel = cheap_blur( inv_parallaxed_UV, object_buffer, 1.0/320.0 );
    vec4 vision_texel = cheap_blur( parallaxed_UV, vision_buffer, (from_c)*(1.0/32.0) );



    //vec4 reflect_texel = texture(reflect_buffer, parallaxed_UV );
    //vec4 reflect_map_texel = texture(reflect_map, (orient + par_mod) - (height_mod*2));
    //vec2 base_reflect_parallaxed_UV = (orient + par_mod) - (height_mod*2);
    //vec4 reflect_map_texel = cheap_blur( base_reflect_parallaxed_UV*0.25, reflect_map, 1.0/256 );


    float exposure = 1.2;
    float ambiance = 0.5;

    vec4 LitObject = object_texel * (light_texel * exposure);
    ///
    //vec4 LitFloor = ( (photon_texel * floor_texel * light_texel) * exposure) + (ambiance*(photon_texel+((clouds(inv_parallaxed_UV)+(light_texel*light_texel))*vision_texel)));
    ///

    
    vec4 LitFloor = ((light_texel+clouds(parallaxed_UV))*(4*photon_texel))+((light_texel*3)*clouds(inv_parallaxed_UV))*floor_texel;

    float mask = 1.0 - LitObject.a;
    vec4 SeenFloor = (LitFloor * vision_texel) * mask;

    LitObject = LitObject * LitObject.a;

    //vec4 combined_light = ((photon_texel + light_texel) * 1.3);

    gl_FragColor = (SeenFloor + LitObject) * vision_texel;
    //gl_FragColor = (clouds(parallaxed_UV)*(4*photon_texel))+(light_texel*clouds(inv_parallaxed_UV))*floor_texel;
//gl_FragColor =light_texel;

}
