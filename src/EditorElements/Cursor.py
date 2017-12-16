from Beagle import API as BGL

class Cursor:
    texture = BGL.assets.get('KT-player/texture/cursor')
    primitive = BGL.primitive.unit_uv_square
    shader = BGL.assets.get('beagle-2d/shader/beagle-2d')
    size = 0.2

    def render(app):
        Cursor.primitive.render_shaded(Cursor.shader, {
            "texBuffer"            : Cursor.texture,
            "translation_local"    : [ 0.0,0.0],
            "scale_local"          : [ Cursor.size,Cursor.size],
            "translation_world"    : [ app.nmx + Cursor.size, app.nmy + Cursor.size ],
            "scale_world"          : [ 1.0,1.0],
            "view"                 : BGL.view.widescreen_16_9,
            "rotation_local"       : 0.0,
            "filter_color"         : [ 1.0,1.0,1.0,1.0 ]
            }
        )
