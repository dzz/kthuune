from Beagle import API as BGL
from .WorldCursor import WorldCursor

class Grid:
    shader = BGL.assets.get('KT-editor/shader/grid')
    texture = BGL.assets.get('KT-editor/texture/grid')
    primitive = BGL.primitive.unit_uv_square
    zoom = 1.0

    cx = 0.0
    cy = 0.0

    def render(app):

        if Grid.zoom == None:
            Grid.zoom = app.camera_zoom
        else:

            a = 0.95
            b = 1.0-a
            Grid.zoom = (Grid.zoom*a) + (app.camera_zoom*b)
            Grid.cx = (Grid.cx*a) + (app.camera_x*b)
            Grid.cy = (Grid.cy*a) + (app.camera_y*b)
        
        Grid.primitive.render_shaded( Grid.shader, { 
            "cam_x"     : float(Grid.cx),
            "cam_y"     : float(Grid.cy),
            "cam_zoom"  : float(Grid.zoom),
            "grid_cell" : Grid.texture
        } )    

        with BGL.blendmode.add:
            WorldCursor.render(app)
