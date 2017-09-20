#version 330

// @description: composite the floor together

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

// Author @patriciogv - 2015
// http://patriciogonzalezvivo.com

//uniform vec2 u_resolution;
//uniform vec2 u_mouse;
//uniform float u_time;

vec2 twist( vec2 buv, float amt ) {

    float a = cos(tick*30.000*amt);

    if(a>0.5) a*=-1;

    float b = sin(tick*54.000*amt);

    if(b<0.2) b = cos(a*tick);

    float c = sin(a*b);
    float d= cos(a+b);

    float da = a*b*c*d;

    vec2 modded = vec2(buv.x,buv.y);

    modded.x += (da*amt)*0.1*amt;
    modded.y += (d*amt)*0.1*amt;
    return modded;
}

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

#define NUM_OCTAVES 8

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

vec4 clouds(vec2 _coord) {


    float ti = tick*0.1;
    vec4 tcol = texture(light_buffer,_coord);
    vec2 coord = _coord;
    coord.x -= 0.5;
    coord.y -= 0.5;

    float damt = length(coord)*2.1*length(tcol);

    //coord*=(1.0+(damt*2));

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


vec4 cheap_blur( sampler2D p_buffer, vec2 p_uv, float p_size ) {

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



vec2 scatter(vec2 UV, float len) {

    return UV;
}

vec2 warpUV( vec2 UV, float minxw, float maxxw,float minyw, float maxyw ) {

    float offsx = ((maxxw-minxw)*UV.y)+minxw;
    float offsy = ((maxyw-minyw)*UV.y)+minyw;
    
    vec2 warped =  vec2( ((UV.x-0.5)*offsx)+0.5, ((UV.y-0.5)*offsy)+0.5);

    return warped;
/*
    vec2 doffs = UV - vec2(0.5,0.5);

    float amt = length(doffs);

    return (warped*amt + UV*(1.0-amt));*/
}


vec2 letterbox(vec2 c, float amt) {

    vec2 o = c;
    o *= (1.0-amt);
    o += (vec2( amt, amt)*0.5);

    return o;
}

vec4 alphablend( vec4 a, vec4 b) {

    vec3 blended = (a*(1.0-b.a)).rgb+(b.rgb*b.a);
    vec4 mixed;
 
    mixed.rgb = blended;

    if((a.a)+(b.a)>0.98) mixed.a = 1.0; else mixed.a = a.a+b.a;

    return mixed;
}


///vec2 Bubble(vec2 buv, float a, float b) {
///
///    vec2 UV = letterbox(buv, b);
///    vec2 UV2 = letterbox(buv,a);
///}


vec4 water() {

    vec2 UV = letterbox(uv, 0.2)*1.5;
    vec2 CUV = (uv-vec2(0.5,0.5))*1.5;

    vec4 dcloud = clouds( CUV*0.001);
    float idx = length(CUV);

    float wt = (tick*0.01)+(0.1*sin(tick*0.01));

    float cd = sin( (idx*20) - wt ); //'sinc esque'

    float vd = cos( ((CUV.y*10)+cd) - wt );

    float hd = cos( ((CUV.x*10)+cd+vd) - wt );


    
    vec4 water_reflect = texture( reflect_map, vec2( vd*cd,hd*cd) + (camera_position*0.01) );
    vec4 cloud = clouds( vec2(vd ,hd ) );
    vec4 l = texture(floor_buffer, vec2( vd*cd, hd*cd ));
    return water_reflect * cloud * l;
}

void xx_main(void) {

    vec2 UV = letterbox(uv, 0.2);
    vec2 UV2 = letterbox(uv,0.23);


    vec2 CUV = (uv-vec2(0.5,0.5));
    float LengthA = length(CUV*0.5)*0.2;
    float LengthB = length(CUV*0.5)*0.3;

    vec2 BubbledUVa= (UV*(1.0-LengthA))+(UV2*LengthA);
    vec2 BubbledUVb= (UV2*(1.0-LengthB))+(UV*LengthA);
    vec2 BubbledUVc= (UV*(1.0-LengthA))+(UV2*LengthB);
    vec2 BubbledUVd= (UV2*(1.0-LengthB))+(UV*LengthB);

    vec4 FloorBase = texture( floor_buffer, BubbledUVa );

    vec4 PhotonBase = texture( photon_buffer, BubbledUVa );
    PhotonBase = PhotonBase*PhotonBase;

    vec4 LightBase = texture( light_buffer, BubbledUVa );
    //LightBase = LightBase * LightBase;

    vec4 ObjectBase = texture( object_buffer, UV ) * ((0.75)+(0.25*(LightBase*0.5) + PhotonBase ));
    //vec4 CanopyBase = texture( canopy_buffer, BubbledUVb );
    vec4 CanopyBase = cheap_blur( canopy_buffer, BubbledUVb, 1.0/512. );

    //vec4 VisionBase = texture( vision_buffer, UV ); 

    vec4 fuzzer = clouds(BubbledUVd);

    vec2 uvfuzzed;
    uvfuzzed.xy = UV.xy;

    uvfuzzed *= 0.98+(fuzzer.r*0.02);
    
    vec4 VisionBase = cheap_blur( vision_buffer, uvfuzzed, 0.01 ); 

    //vec4 VisionBase = vec4(1.0,1.0,1.0,1.0);

    vec4 FogLit = clouds(BubbledUVd) * LightBase * PhotonBase;
    FogLit.a = 0.2;

    vec4 LitFloor = alphablend( FloorBase * ( PhotonBase + LightBase ) * VisionBase, FogLit ) * 1.5;
    //LitFloor = FloorBase;
    vec4 PopupMerged = alphablend( LitFloor, ObjectBase );

    vec4 CanopyLit = CanopyBase * PhotonBase * VisionBase;
    CanopyLit.a = CanopyBase.a;
    vec4 CanopyMerged = alphablend( PopupMerged, CanopyLit );

    vec4 CloudLit = clouds(BubbledUVc) * (PhotonBase + (LightBase*LightBase));
    CloudLit.a = 1.0 - min((VisionBase.r*VisionBase.r)*20.0,1.0);
    CloudLit.r = 0.6 * (1.0-uv.y) * LengthA;
    CloudLit.g = 0.6 * (1.0-uv.y) * LengthA;
    CloudLit.b = 0.6 * (1.0-uv.y) * LengthA;

    if(( FloorBase.a < 0.05) && ObjectBase.a < 0.05) {
        gl_FragColor = water();
    } else {
        gl_FragColor = alphablend( CanopyMerged, CloudLit );
    }

    //gl_FragColor = vec4( Length, Length, Length, 1.0 );
}




///////////////void xxxmain(void) {
///////////////
///////////////
///////////////    vec2 UV = letterbox(uv, 0.3);
///////////////    vec2 CUV = (UV-vec2(0.5,0.5))*2;
///////////////
///////////////    //haxx
///////////////    float from_c = (length(CUV * vec2(1.7,1.0)))*1.2;
///////////////    float parallax_ratio = 0.1*from_c;
///////////////    vec2 PUV = ((UV-vec2(0.5,0.5)) * (1.0+(parallax_ratio * from_c ))) + vec2(0.5,0.5);
///////////////
///////////////    vec4 Clouds1 = clouds( warpUV( PUV, 0.8,1.3,0.8,1.3) );
///////////////    vec4 Clouds2 = clouds( warpUV( PUV, 0.8,1.5,0.8,1.5) );
///////////////
///////////////    float Length = length(CUV*0.5);
///////////////
///////////////    Clouds1.a = Length;
///////////////    Clouds2.a = Length*0.5;
///////////////
///////////////    {
///////////////        vec4 VisionTexel = texture( vision_buffer, twist(UV, from_c) );
///////////////        float c1Exposure = 3.0;
///////////////        float c2Exposure = 2.0;
///////////////        vec4 CloudPhoton = (texture( photon_buffer, UV )*c1Exposure);
///////////////        CloudPhoton.a = 1.0;
///////////////        Clouds1 = Clouds1 * CloudPhoton * VisionTexel;
///////////////        vec4 CloudLight =  (texture( light_buffer, UV )*c2Exposure);
///////////////        CloudLight.a = 1.0;
///////////////        Clouds2 = Clouds2 * CloudLight * VisionTexel;
///////////////    }
///////////////
///////////////
///////////////    vec4 BlurredObject;
///////////////    {
///////////////        vec2 BOUV1 = warpUV( PUV, 1.1,0.9,1.1,0.9 );
///////////////        vec2 BOUV2 = warpUV( PUV, 0.9,1.1,0.9,1.1 );
///////////////        BlurredObject = (cheap_blur( BOUV1, object_buffer, 1.0/512 ) + cheap_blur( BOUV2, object_buffer, 1.0/256))/2.0;
///////////////
///////////////        BlurredObject = vec4(1.0,1.0,1.0,2.0) - vec4( BlurredObject.a, BlurredObject.a, BlurredObject.a, 1.0);
///////////////
///////////////    }
///////////////    //vec4 LDebug = vec4(Length,Length,Length,1.0);
///////////////    vec4 FloorMerged;
///////////////    {
///////////////        vec2 FloorUV = warpUV( PUV, 0.8,1.2,0.8,1.2);
///////////////        vec4 FloorBase = texture( floor_buffer, FloorUV );
///////////////
///////////////        vec4 FloorLight = alphablend( texture( light_buffer, FloorUV ), Clouds1 );
///////////////        vec4 FloorPhoton = texture( photon_buffer, FloorUV );
///////////////        vec4 VisionTexel = texture( vision_buffer, twist(FloorUV, from_c) );
///////////////
///////////////        FloorMerged = FloorPhoton;
///////////////
///////////////        float FloorBaseExposure = 75;
///////////////        FloorLight = (FloorLight * FloorPhoton) * FloorBaseExposure;
///////////////
///////////////        float FloorMax = 1;
///////////////        //FloorMerged = smoothstep(0.0, FloorMax, ((FloorBase) * FloorLight)) * VisionTexel * BlurredObject;
///////////////    }
///////////////
///////////////    vec4 PopupMerged;
///////////////    {
///////////////        vec2 PopupUV = warpUV( UV, 0.95,1.05,0.95,1.05 );
///////////////        vec2 LightUV = UV;
///////////////        PopupMerged = texture( object_buffer, PopupUV );
///////////////
///////////////        float PopupLightExposure = 1.2;
///////////////        float PopupAmbientExposure = 0.004;
///////////////
///////////////        vec4 PopupPhoton = texture(reflect_map, PopupUV ) * PopupAmbientExposure;
///////////////
///////////////        PopupMerged.rgb += (PopupPhoton.rgb)*(PopupMerged.a);
///////////////
///////////////        vec4 PopupLight = texture(light_buffer, PopupUV) * PopupLightExposure;
///////////////
///////////////        vec3 lit = PopupMerged.rgb * PopupLight.rgb;
///////////////
///////////////        PopupMerged.rgb = lit;
///////////////        vec4 VisionTexel = texture( vision_buffer, UV );
///////////////        PopupMerged*= VisionTexel;
///////////////    }
///////////////
///////////////
///////////////    vec4 FloorPopupMixed;
///////////////    {
///////////////        /*vec3 FloorPopupBlended = (FloorMerged*(1.0-PopupMerged.a)).rgb+(PopupMerged.rgb*PopupMerged.a);
///////////////
///////////////        FloorPopupMixed.rgb = FloorPopupBlended;
///////////////        FloorPopupMixed.a = 1.0;*/
///////////////        FloorPopupMixed = alphablend( FloorMerged, PopupMerged );
///////////////    }
///////////////
///////////////    vec4 CanopyMerged;
///////////////    {
///////////////        vec2 CanopyUV = warpUV( UV, 0.7,1.5,0.7,1.5);
///////////////        vec4 CanopyBase = texture(canopy_buffer, CanopyUV);
///////////////        vec4 CanopyPhoton = texture(photon_buffer, CanopyUV );
///////////////
///////////////        float CanopyExposure = 1;
///////////////        vec4 CanopyLit = CanopyBase * (CanopyPhoton*CanopyExposure);
///////////////        CanopyMerged = alphablend( FloorPopupMixed, CanopyLit );
///////////////        CanopyMerged = alphablend( CanopyMerged, Clouds2 );
///////////////        vec4 VisionTexel = texture( vision_buffer, CanopyUV );
///////////////        CanopyMerged *= VisionTexel;
///////////////    }
///////////////
///////////////    gl_FragColor = CanopyMerged;
///////////////    //gl_FragColor = CanopyMerged*6;
///////////////    //////////////gl_FragColor = FloorMerged + PopupMerged;
///////////////}

//this is the main that is most representitive of the current design as of sep 4th 2017
void main(void) {


    vec2 UV = vec2(0.1,0.1)+(uv*0.8);

    vec2 inv_UV = UV;
    float x_scale = 0.9+(0.3*(UV.y*UV.y));
    UV.x -= 0.5;
    UV.x *= x_scale;
    UV.x += 0.5;
    inv_UV.x -= 0.5;
    inv_UV.x *= 2.0-x_scale;
    inv_UV.x += 0.5;

    vec2 centered_UV = (UV+vec2(-0.5,-0.5))*2;
    centered_UV*= centered_UV;

    float from_c = (length(centered_UV * vec2(1.7,1.0)))*1.2;
    float parallax_ratio = 0.01*from_c;

    from_c = from_c*from_c;

    vec2 parallaxed_UV = ((UV-vec2(0.5,0.5)) * (1.0+(parallax_ratio * from_c ))) + vec2(0.5,0.5);
    vec2 inv_parallaxed_UV = ((inv_UV-vec2(0.5,0.5)) * (1.0+(parallax_ratio * (1.7-from_c) ))) + vec2(0.5,0.5);

    //hack test
    //UV = vec2(0.1,0.1)+(uv*0.8);
    //parallaxed_UV = UV;
    //inv_parallaxed_UV = UV;



    vec4 photon_texel =  texture(photon_buffer, UV);
    vec4 floor_texel = texture(floor_buffer,parallaxed_UV);
    vec4 light_texel = texture( light_buffer, UV);
    vec4 shadow_texel = texture( shadow_buffer, UV);

    vec4 object_texel = texture( object_buffer, inv_parallaxed_UV);
    //vec4 canopy_texel = texture( object_buffer, inv_parallaxed_UV);
    vec4 vision_texel = texture( vision_buffer, parallaxed_UV);


    float exposure = 1.2;
    float ambiance = 0.5;

    vec4 LitObject = object_texel * (light_texel * exposure);
    ///
    //vec4 LitFloor = ( (photon_texel * floor_texel * light_texel) * exposure) + (ambiance*(photon_texel+((clouds(inv_parallaxed_UV)+(light_texel*light_texel))*vision_texel)));
    ///

    
    //vec4 LitFloor = ((light_texel+clouds(parallaxed_UV))*(4*photon_texel))+((light_texel*3)*clouds(inv_parallaxed_UV))*floor_texel;

    vec4 LitFloor = light_texel;

    float mask = 1.0 - LitObject.a;
    vec4 SeenFloor = (((0.6*water())+0.4)*LitFloor * vision_texel) * mask;

    LitObject = LitObject * LitObject.a;
    
    //vec4 combined_light = ((photon_texel + light_texel) * 1.3);

    vec4 background = texture( reflect_map, (inv_parallaxed_UV*0.8* ((UV.y*0.2)+0.7)) + (from_c*camera_position *-0.001 * ((UV.y*0.3)+0.7) ));

    //background = background + water();

    vec4 merged_light = light_texel * shadow_texel;
    merged_light.a = 1.0;
    SeenFloor = (merged_light) * floor_texel;
    gl_FragColor = alphablend( SeenFloor, LitObject);
    //gl_FragColor = shadow_texel;

    //gl_FragColor = (clouds(parallaxed_UV)*(4*photon_texel))+(light_texel*clouds(inv_parallaxed_UV))*floor_texel;
//gl_FragColor =light_texel;

}

/////// void main(void) {
/////// 
/////// //this is the main that is most representitive of the current design as of sep 4th 2017
/////// 
///////     vec2 UV = vec2(0.1,0.1)+(uv*0.8);
/////// 
///////     vec2 inv_UV = UV;
///////     float x_scale = 0.8+(0.6*(UV.y*UV.y));
///////     UV.x -= 0.5;
///////     UV.x *= x_scale;
///////     UV.x += 0.5;
///////     inv_UV.x -= 0.5;
///////     inv_UV.x *= 2.0-x_scale;
///////     inv_UV.x += 0.5;
/////// 
///////     vec2 centered_UV = (UV+vec2(-0.5,-0.5))*2;
///////     centered_UV*= centered_UV;
/////// 
///////     float from_c = (length(centered_UV * vec2(1.7,1.0)))*1.2;
///////     float parallax_ratio = 0.001*from_c;
/////// 
///////     from_c = from_c*from_c;
/////// 
///////     vec2 parallaxed_UV = ((UV-vec2(0.5,0.5)) * (1.0+(parallax_ratio * from_c ))) + vec2(0.5,0.5);
///////     vec2 inv_parallaxed_UV = ((inv_UV-vec2(0.5,0.5)) * (1.0+(parallax_ratio * (1.7-from_c) ))) + vec2(0.5,0.5);
/////// 
/////// 
/////// 
///////     vec4 photon_texel =  texture(photon_buffer, UV);
///////     vec4 floor_texel = texture(floor_buffer,parallaxed_UV);
///////     vec4 light_texel = texture( light_buffer, UV);
///////     vec4 object_texel = texture( object_buffer, inv_parallaxed_UV);
///////     vec4 vision_texel = texture( vision_buffer, parallaxed_UV);
/////// 
/////// 
///////     float exposure = 1.2;
///////     float ambiance = 0.5;
/////// 
///////     vec4 LitObject = object_texel * (light_texel * exposure);
///////     ///
///////     //vec4 LitFloor = ( (photon_texel * floor_texel * light_texel) * exposure) + (ambiance*(photon_texel+((clouds(inv_parallaxed_UV)+(light_texel*light_texel))*vision_texel)));
///////     ///
/////// 
///////     
///////     vec4 LitFloor = ((light_texel+clouds(parallaxed_UV))*(4*photon_texel))+((light_texel*3)*clouds(inv_parallaxed_UV))*floor_texel;
/////// 
///////     float mask = 1.0 - LitObject.a;
///////     vec4 SeenFloor = (LitFloor * vision_texel) * mask;
/////// 
///////     LitObject = LitObject * LitObject.a;
///////     
///////     //vec4 combined_light = ((photon_texel + light_texel) * 1.3);
/////// 
///////     gl_FragColor = (SeenFloor + LitObject) * vision_texel;
///////     //gl_FragColor = (clouds(parallaxed_UV)*(4*photon_texel))+(light_texel*clouds(inv_parallaxed_UV))*floor_texel;
/////// //gl_FragColor =light_texel;
/////// 
/////// }



///JULY 7th --- A VERSIon of thE FLOOr thaT WE LIKE A LOT

///// void main(void) {
///// 
/////     vec2 CUV = (uv-vec2(0.5,0.5))*2;
/////     vec2 FloorUV = uv;
///// 
/////     vec4 FloorBase = texture( floor_buffer, FloorUV );
/////     vec4 FloorLight = texture( light_buffer, FloorUV );
/////     vec4 FloorPhoton = texture( photon_buffer, FloorUV ) * clouds(CUV);
///// 
/////     float FloorBaseExposure = 75;
/////     FloorLight = FloorLight + (FloorLight * FloorPhoton) * FloorBaseExposure;
///// 
/////     float FloorMax = 1;
///// 
/////     vec4 FloorMerged = smoothstep(0.0, FloorMax, ((FloorBase) * FloorLight));
///// 
/////     gl_FragColor = FloorMerged;
///// }
