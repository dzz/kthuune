
in vec2 uv;

void main() {
    
    vec2 UV = vec2(uv.x, 1.0-uv.y);
    float height = 0.023;
    float width = 0.2;
    
    gl_FragColor = vec4(0.0,0.0,0.0,0.0);
    if(UV.y<height) {
        gl_FragColor.rgb = (UV.y/height)*vec3(1.0,1.0,1.0)*0.5;
        gl_FragColor.a = 1.0;
    }

    if((1.0-UV.y)<height) {
        gl_FragColor.rgb = ((1.0-UV.y)/height)*vec3(1.0,1.0,1.0)*0.5;
        gl_FragColor.a = 1.0;
    }
        
}
