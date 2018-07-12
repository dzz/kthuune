from Beagle import API as BGL
from .StatusCards import Card
from .Hud import Hud

class PotionCountView():
    shader = BGL.assets.get("beagle-2d/shader/beagle-2d")
    
    def __init__(self,player):
        self.fb = BGL.framebuffer.from_dims( (8*3)+2, 10 )
        self.player = player

    def render(self):
        with BGL.context.render_target(self.fb):
            with BGL.blendmode.alpha_over:
                BGL.context.clear(0.0,0.0,0.0,0.0)
                BGL.lotext.render_text_pixels("x{0}".format(self.player.health_count),1,1,[1.0,0.0,0.0])
        with BGL.blendmode.alpha_over:
            Card.primitive.render_shaded( PotionCountView.shader, self.get_shader_params() )

    def get_shader_params(self):
        return {
            "texBuffer"            : self.fb,
            "translation_local"    : [ 0, 0 ],
            "scale_local"          : [ 3.0*0.25,-1.0*0.25 ],
            "translation_world"    : [ -5.85,-2.8],
            "scale_world"          : [1.0,1.0],
            "view"                 : Hud.view,
            "rotation_local"       : 0.0,
            "filter_color"         : [1.0,1.0,1.0,1.0],
            "uv_translate"         : [ 0,0 ] }
