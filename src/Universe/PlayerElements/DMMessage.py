from Beagle import API as BGL

class DMMessage():

    primitive = BGL.primitive.unit_uv_square
    shader = BGL.assets.get("beagle-2d/shader/beagle-2d")

    def __init__(self,message):
        self.buffer = BGL.framebuffer.from_dims( 8*len(message)+2,10)
        with BGL.context.render_target( self.buffer ):
            BGL.context.clear(0.0,0.0,0.0,1.0)
            with BGL.blendmode.alpha_over:
                BGL.lotext.render_text_pixels(message,1,1,[ 1.0,1.0,1.0 ])
        self.width = len(message)
        self.char_s = 0.08
            
    def render(self, index, log_size):

        fpi = (index+1) / log_size
        shader_params = {
            "texBuffer"            : self.buffer,
            "translation_local"    : [ 0, 0 - float(index)*1.5 ],
            "scale_local"          : [ (self.width*self.char_s)+(fpi*0.2),-1*self.char_s ],
            "translation_world"    : [ 0.0,-4.5+(fpi*0.2) ],
            "scale_world"          : [ 1.0,1.0],
            "view"                 : Hud.view,
            "rotation_local"       : 0.0,
            "filter_color"         : [ fpi ,1.0-fpi,fpi,fpi],
            "uv_translate"         : [ 0,0 ] }
        DMMessage.primitive.render_shaded( DMMessage.shader, shader_params )
        
