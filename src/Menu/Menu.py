from Beagle import API as BGL

class Menu:
    texture_title = BGL.assets.get("KT-player/texture/menu_title")
    primitive = BGL.primitive.unit_uv_square
    shader = BGL.assets.get("KT-player/shader/menu_base")
    t = 0.0

    def tick():
        Menu.t += 0.003;
        if(Menu.t>1000):
            Menu.t = 0
    
    def render():
        with BGL.blendmode.alpha_over:
            Menu.primitive.render_shaded( Menu.shader, {
                "texBuffer" : Menu.texture_title,
                "tick" : Menu.t
            })
