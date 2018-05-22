from Beagle import API as BGL
from .Hud import Hud

class TerminalRenderer():
    shader = BGL.assets.get("KT-player/shader/terminal")
    primitive = BGL.primitive.unit_uv_square
    texbuffer = BGL.framebuffer.from_dims(320,240)
    windowtex = BGL.assets.get("KT-player/texture/terminal0000")
    window_shader = BGL.assets.get("beagle-2d/shader/passthru_inv")

    def render(size, tick, terminal):
        with BGL.context.render_target( TerminalRenderer.texbuffer ):
            BGL.context.clear(0.0,0.0,0.0,1.0)
            TerminalRenderer.primitive.render_shaded(
                TerminalRenderer.window_shader,
                { "texBuffer" : TerminalRenderer.windowtex }
            )
            if(terminal):
                BGL.lotext.render_text_pixels( terminal.title, 6,9, [0.0,0.0,0.0] )
                terminal.render_ui()
        TerminalRenderer.primitive.render_shaded(TerminalRenderer.shader, TerminalRenderer.get_shader_params(size,tick))


    def get_shader_params(size, tick):
        return {
            "tick" : [ tick ],
            "size" : size,
            "texBuffer"            : TerminalRenderer.texbuffer,
            "translation_local"    : [ 0, 0 ],
            "scale_local"          : [ 3.2*1.25,-2.4*size*1.25 ],
            "translation_world"    : [ 0, 0 ],
            "scale_world"          : [1.0+(2.0*(1.0-size)),1.0],
            "view"                 : Hud.view,
            "rotation_local"       : 0.0,
            "filter_color"         : [1.0,1.0,1.0,size*0.5],
            "uv_translate"         : [ 0,0 ] }
