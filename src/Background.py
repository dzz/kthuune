from Beagle import API as BGL

class Background:
    shader = BGL.assets.get("KT-compositor/shader/background")
    bg_texture = BGL.assets.get("KT-forest/texture/lightmap")
    sky_texture = BGL.assets.get("KT-forest/texture/background")
    parallax_sky = 0.005
    parallax_bg = 0.01

    primitive = BGL.primitive.unit_uv_square
    def render(self, vision_tex):
        Background.primitive.render_shaded( Background.shader, {
            "bg_texture" : Background.sky_texture,
            "camera_position" : self.camera.p,
            "parallax" : [ Background.parallax_sky/4 ],
            "vision_tex" : vision_tex
        } )
        with BGL.blendmode.alpha_over:
            Background.primitive.render_shaded( Background.shader, {
                "bg_texture" : Background.bg_texture,
                "camera_position" : self.camera.p,
                "parallax" : [ Background.parallax_bg/4 ],
                "vision_tex" : vision_tex
            } )
        return True
