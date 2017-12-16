from Beagle import API as BGL
from math import floor

class WorldCursor:
    texture = BGL.assets.get('KT-editor/texture/worldcursor')
    primitive = BGL.primitive.unit_uv_square
    shader = BGL.assets.get('beagle-2d/shader/beagle-2d')
    size = 0.2

    def render(app):

        cx,cy = app.nmx, app.nmy

        cx, cy = app.scr_to_world(cx,cy)

        cx += 0.5
        cy += 0.5

        cx = floor(cx)
        cy = floor(cy)

        cx, cy = app.world_to_scr(cx,cy)

        sz = WorldCursor.size / (1.0/app.camera_zoom)
        WorldCursor.primitive.render_shaded(WorldCursor.shader, {
            "texBuffer"            : WorldCursor.texture,
            "translation_local"    : [ 0.0,0.0],
            "scale_local"          : [ sz,sz],
            "translation_world"    : [ cx,cy ],
            "scale_world"          : [ 1.0,1.0],
            "view"                 : BGL.view.widescreen_16_9,
            "rotation_local"       : 0.0,
            "filter_color"         : [ 0.5,0.5,0.5,1.0 ]
            }
        )
