from Newfoundland.Object import Object
from Beagle import API as BGL
from random import uniform

class AttackInfo(Object):
    def customize(self):
        self.tick_type = Object.TickTypes.PURGING
        self.buffer = BGL.framebuffer.from_dims( len(self.message)*8, 8)
        self.texture = self.buffer.get_texture()      
        self.buftarget = "hud"
        self.size = [ 1.0*len(self.message), -1.0 ]

        self.lifetime = 100
        with BGL.context.render_target(self.buffer):
            BGL.context.clear(0.0,0.0,0.0,0.0)
            BGL.lotext.render_text_pixels( self.message, 0,0, [1.0,1.0,1.0] )

    def tick(self):
        if self.lifetime<60:
            self.size[0] *= 1.28
            self.size[1] *= 1.28
    
        if self.lifetime<80:
            self.color[3] = self.color[3]*0.95
            self.color[0] = uniform(0.0,1.0)
            self.color[1] = uniform(0.0,1.0)
            self.color[2] = uniform(0.0,1.0)

        if self.lifetime>0:
            self.lifetime -=1
            return True
        else:
            self.floor.objects.remove(self)
            return False
