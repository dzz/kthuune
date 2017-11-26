vec4 correct_vision( vec4 vision_texel ) {

    vision_texel.rgb -= vec3(0.5,0.5,0.5);
    vision_texel.rgb*= 2.0;
    vision_texel.rgb+= vec3(0.5,0.5,0.5);

    return smoothstep( vec4(0.0,0.0,0.0,1.0), vec4( 1.5,1.5,1.5,1.5), vision_texel );
}
