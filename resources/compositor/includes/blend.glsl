vec4 alphablend( vec4 a, vec4 b) {

    vec3 blended = (a*(1.0-b.a)).rgb+(b.rgb*b.a);
    vec4 mixed;
 
    mixed.rgb = blended;

    if((a.a)+(b.a)>0.98) mixed.a = 1.0; else mixed.a = a.a+b.a;

    return mixed;
}
