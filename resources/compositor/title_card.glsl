#version 330

// @description: passes through texture pixels unchanged

in vec2 uv;
uniform float tick;

void main(void) {

    gl_FragColor = vec4(0.0,0.0,0.0,0.0);
    if(tick<60) {
        gl_FragColor = vec4(0.0,0.0,0.0,1.0);
    }
    else {
        float t = (tick-200)/(500-200);

        t = 1.0-t;
        t=t*t*t;
        t = 1.0-t;
        if(uv.y<0.3333) {
            if(uv.x<1.0-t)
            gl_FragColor = vec4(0.0,0.0,0.0,1.0);
        } else if(uv.y<0.6666) {
            if(uv.x>t)
            gl_FragColor = vec4(0.0,0.0,0.0,1.0);
        } else {
            if(uv.x<1.0-t)
            gl_FragColor = vec4(0.0,0.0,0.0,1.0);
        }
    }
}

