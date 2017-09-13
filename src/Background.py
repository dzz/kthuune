from Beagle import API as BGL

class Background:
    shader = BGL.assets.get("KT-compositor/shader/background")
    bg_texture = BGL.assets.get("KT-forest/texture/lightmap")
    primitive = BGL.primitive.unit_uv_square
    def render(self):
        Background.primitive.render_shaded( Background.shader, {
            "bg_texture" : Background.bg_texture,
            "camera_position" : self.camera.p
        } )
        return True
