in vec2 uv;
uniform float cam_x;
uniform float cam_y;
uniform float cam_zoom;

uniform sampler2D grid_cell;


void main() {

    vec2 UV = uv;

    UV -= vec2(0.5,0.5);
    UV *= vec2(16,9);

    UV.x += cam_x;
    UV.y += cam_y;
    UV *= 1.0 / cam_zoom;
    
    float x_mod = mod(UV.x,1.0);
    float y_mod = mod(UV.y,1.0);

    gl_FragColor = texture( grid_cell, vec2(x_mod, y_mod));
}

