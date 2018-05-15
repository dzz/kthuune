#version 330

// @description: composite the floor together

// @load "includes/uvs.glsl"
// @load "includes/blend.glsl"
// @load "includes/lighting.glsl"
// @load "includes/noise.glsl"
// @load "includes/vision.glsl"

uniform float tick;
uniform float fuzz_amt;
uniform float target_width;
uniform float target_height;

uniform vec2 camera_position;

uniform sampler2D floor_buffer;
uniform sampler2D light_buffer;
uniform sampler2D object_buffer;
uniform sampler2D vision_buffer;
uniform sampler2D photon_buffer;
uniform sampler2D reflect_map;
uniform sampler2D canopy_buffer;
uniform sampler2D shadow_buffer;

in vec2 uv;

void main() {

    vec2 noisey_offset = vec2(0.0,0.0);
    //if(fuzz_amt>0.0001) {
    //    float d_amt = get_uv_len(uv)*fuzz_amt;
    //    noisey_offset = vec2( random(uv*1000+tick), random(uv*-3000+tick))*(d_amt*d_amt*d_amt*0.3);// *(1.0+(sin(uv.y*200)*cos(uv.x*200)*0.1));
    //} 

/*
        float r_amt = 0.01*(2.0-get_uv_len(uv));
        vec2 refl_offset = vec2( random(uv*1000+tick), random(uv*-3000+tick))*r_amt;*/

    vec2 floor_uv = get_floor_uv(uv+noisey_offset);
    vec4 floor_texel = texture( floor_buffer, floor_uv );
    //vec4 reflect_texel = texture( reflect_map, (floor_uv+(camera_position*3))+refl_offset );

    vec4 vision_texel = correct_vision( texture( vision_buffer, floor_uv)); 

    vec4 light_texel = texture( light_buffer, floor_uv )*vision_texel;
    vec4 shadow_texel = texture( shadow_buffer, floor_uv);

    vec4 object_drop_hint = texture( object_buffer, floor_uv - (vec2(0.01,0.01)*length(floor_uv)));

    light_texel *= 1.0-(object_drop_hint.a*0.25);

    light_texel.rgb*= (shadow_texel.a*shadow_texel.rgb);


/*
    if(length(floor_texel.rgb)>1.7) {
        floor_texel.rgb+=(reflect_texel.rgb*light_texel.rgb*vision_texel.rgb);
    }*/

    vec2 object_uv = get_parallax_uv(uv+noisey_offset);
    vec4 object_texel = texture( object_buffer, object_uv );
    vec4 object_light_texel = texture( light_buffer, object_uv );

    floor_texel.rgb *= vision_texel.r;
    floor_texel.rgb *= expose(light_texel.rgb);

    //object_texel.rgb *= expose(object_light_texel.rgb);

    gl_FragColor = alphablend( floor_texel, object_texel);
}
