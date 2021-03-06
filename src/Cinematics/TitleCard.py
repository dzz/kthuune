from Beagle import API as BGL
from random import uniform

class TitleCard():
    primitive = BGL.primitive.unit_uv_square
    shader = BGL.assets.get("KT-compositor/shader/title_card")

    def __init__(self):
        self.hud_buffer = BGL.framebuffer.from_dims(426,240)
        self.tval = 0
        self.title = "Oort Cloud"
        self.shader_tval = 0
        self.centerx = 64
        self.top = 120 

    def reset(self, title, shader = True):
        with BGL.context.render_target( self.hud_buffer ):
            BGL.context.clear( 0.0,0.0,0.0,0.0 )
        self.tval = 0
        if(shader):
            self.shader_tval = 0
        else:
            self.shader_tval = 700
        self.title = title

    def displaying(self):
        if(self.tval<450):
            return True
        return False

    def center_x(self):
        return self.centerx

    def render(self):

        shadow_color = [ 0.0,0.0,0.5]
        fg_color = [ 1.0,1.0,1.0]

        if(self.tval>200):
            t = (self.tval-200)/100
            t = 1.0-t
            fg_color[0] *= t 
            fg_color[1] *= t 
            fg_color[2] *= t 
            shadow_color[1] *= t 

            if((1.0-t)>0.8):
                fg_color[0] += uniform(0.0,5.8*t)
                fg_color[1] += uniform(0.0,5.8*t)
                fg_color[2] += uniform(0.0,5.8*t)

        if(self.tval<700):
            TitleCard.primitive.render_shaded( TitleCard.shader, { "tick" : min(float(self.shader_tval),700.0) } )
            if(self.tval<300):
                with BGL.context.render_target( self.hud_buffer ):
                    BGL.lotext.render_text_pixels(self.title, self.center_x(),self.top-4,shadow_color )
                    BGL.lotext.render_text_pixels(self.title, self.center_x(),self.top-3,fg_color )
                self.hud_buffer.render_processed( BGL.assets.get("beagle-2d/shader/passthru") )

    def tick(self):
        self.tval = self.tval+1
        self.shader_tval = self.shader_tval + 1
    
    def abort(self):
        self.tval = 701

