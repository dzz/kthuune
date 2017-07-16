from client.beagle.beagle_api import api as bgl

class uniform_fade():
    primitive = bgl.primitive.unit_uv_square
    shader = bgl.assets.get("KT-compositor/shader/fadetowhite")

    def apply_fadeout( amount ):
        uniform_fade.primitive.render_shaded( uniform_fade.shader, { "amt" : amount } )
