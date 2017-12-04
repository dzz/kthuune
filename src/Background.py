from Beagle import API as BGL

class Background:
    shader = BGL.assets.get("KT-compositor/shader/background")
    bg_texture = BGL.assets.get("KT-forest/texture/lightmap")
    sky_texture = BGL.assets.get("KT-forest/texture/background")
    parallax_sky = 0.005
    parallax_bg = 0.01
    primitive = BGL.primitive.unit_uv_square
    add_blending = False

    def __init__(self):
        self.bg_texture = None
        self.sky_texture = None

    def render(self, vision_tex):


        if(self.bg_texture is None):
             self.bg_texture = Background.bg_texture
        if(self.sky_texture is None):
             self.sky_texture = Background.sky_texture

        Background.shader.last_bound = {} # hack to force rebinding....
        Background.primitive.render_shaded( Background.shader, {
            "bg_texture" : self.sky_texture,
            "camera_position" : self.camera.p,
            "parallax" : [ Background.parallax_sky/4 ],
            "vision_tex" : vision_tex
        } )
        Background.shader.last_bound = {} # hack to force rebinding....

        if not Background.add_blending:
            with BGL.blendmode.alpha_over:
                Background.primitive.render_shaded( Background.shader, {
                    "bg_texture" : self.bg_texture,
                    "camera_position" : self.camera.p,
                    "parallax" : [ Background.parallax_bg/4 ],
                    "vision_tex" : vision_tex
                } )
        else:
            Background.primitive.render_shaded( Background.shader, {
                "bg_texture" : self.sky_texture,
                "camera_position" : self.camera.p,
                "parallax" : [ Background.parallax_sky/3 ],
                "vision_tex" : vision_tex
            } )
            with BGL.blendmode.add:
                Background.primitive.render_shaded( Background.shader, {
                    "bg_texture" : self.bg_texture,
                    "camera_position" : self.camera.p,
                    "parallax" : [ Background.parallax_bg/4 ],
                    "vision_tex" : vision_tex
                } )
                Background.primitive.render_shaded( Background.shader, {
                    "bg_texture" : self.bg_texture,
                    "camera_position" : self.camera.p,
                    "parallax" : [ Background.parallax_bg/3 ],
                    "vision_tex" : vision_tex
                } )
        return True
