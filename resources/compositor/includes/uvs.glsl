vec2 letterbox_uv( vec2 uv, float amt ) {

    uv*=amt;
    float buf = (1.0-amt)/2;
    uv+=vec2( buf,buf);
    return uv;
}


vec2 get_fisheye_uv( vec2 uv, float a, float b ) {

    return uv;

    vec2 big_uv = letterbox_uv( uv, a);
    vec2 small_uv = letterbox_uv( uv, b);
    uv-= vec2(0.5,0.5);
    float l = (uv.x*uv.x)+(uv.y*uv.y);
    return (small_uv*l)+((1.0-l)*big_uv);

}
vec2 get_floor_uv( vec2 uv ) {
    return get_fisheye_uv( uv, 0.75, 0.95 );
}

vec2 get_parallax_uv( vec2 uv ) {

    vec2 inv_fisheye = get_fisheye_uv( uv, 0.95,0.75);
    vec2 floor_uv = get_floor_uv(uv);
    float l = length(uv);
    return (l*floor_uv)+((1.0-l)*inv_fisheye);
}

vec2 get_centered_uv( vec2 uv) {
    return uv-vec2(0.5,0.5);
}

float get_uv_len( vec2 uv) {
    return length(get_centered_uv(uv));
}
