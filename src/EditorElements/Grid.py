from Beagle import API as BGL

class Grid:
    shader = BGL.assets.get('KT-editor/shader/grid')
    texture = BGL.assets.get('KT-editor/texture/grid')
    primitive = BGL.primitive.unit_uv_square
    zoom = None

    def render(app):

        if Grid.zoom == None:
            Grid.zoom = app.camera_zoom
        else:
            Grid.zoom = (Grid.zoom*0.9) + (app.camera_zoom*0.1)
        
        Grid.primitive.render_shaded( Grid.shader, { 
            "cam_x"     : float(app.camera_x),
            "cam_y"     : float(app.camera_y),
            "cam_zoom"  : float(Grid.zoom),
            "grid_cell" : Grid.texture
        } )    
