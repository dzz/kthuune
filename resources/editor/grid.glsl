#version 330

in vec2 uv;
uniform float cam_x;
uniform float cam_y;
uniform float cam_zoom;
uniform float w_size;

uniform sampler2D grid_cell;


void main() {

    vec2 UV = uv;

    UV -= vec2(0.5,0.5);
    UV *= vec2(16,9);

    UV *= 1.0 / cam_zoom;
    UV.x += cam_x;
    UV.y -= cam_y;
    
    float x_mod = mod(UV.x,1.0);
    float y_mod = mod(UV.y,1.0);


    gl_FragColor = vec4(0.0,0.0,0.0,1.0);

    if(w_size!=0.0) {
        if(abs(UV.x)<w_size)
            if(abs(UV.y)<w_size)
                gl_FragColor = texture( grid_cell, vec2(x_mod, y_mod));
    }

}

