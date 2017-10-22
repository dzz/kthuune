#version 330

// @description: composite the floor together

// @load "includes/uvs.glsl"
// @load "includes/blend.glsl"
// @load "includes/lighting.glsl"

uniform float tick;
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

    vec2 floor_uv = get_floor_uv(uv);
    vec4 floor_texel = texture( floor_buffer, floor_uv );
    vec4 vision_texel = texture( vision_buffer, floor_uv); 
    vec4 light_texel = texture( light_buffer, floor_uv );

    vec2 object_uv = get_parallax_uv(uv);
    vec4 object_texel = texture( object_buffer, object_uv );
    vec4 object_light_texel = texture( light_buffer, object_uv );

    floor_texel.rgb *= vision_texel.r;
    floor_texel.rgb *= expose(light_texel.rgb);

    object_texel.rgb *= expose(light_texel.rgb);

    gl_FragColor = alphablend( floor_texel, object_texel);
}