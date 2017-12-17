in vec2 uv;
uniform float open_amt;

void main() {
    
    vec2 UV = vec2(uv.x, 1.0-uv.y);
    float width = 0.2*open_amt;
    
    gl_FragColor = vec4(0.0,0.0,0.0,0.0);
    if(UV.x<width) {
        gl_FragColor.rgb = (UV.x/width)*vec3(1.0,1.0,1.0)*0.5;
        gl_FragColor.a = 0.8*open_amt;
    }
        
}
