from Newfoundland.Object import Object
from random import choice, uniform
from Beagle import API as BGL
from math import sin,cos

class SplatterParticle(Object):
    texture = [
        BGL.assets.get("KT-forest/texture/blood0000"),
        BGL.assets.get("KT-forest/texture/blood0001"),
        BGL.assets.get("KT-forest/texture/blood0002"),
        BGL.assets.get("KT-forest/texture/blood0003"),
    ]
    def __init__(self,**kwargs):
        Object.__init__(self,**kwargs)

        self.texture = choice(SplatterParticle.texture)

        if "ptexture" in self.__dict__:
            self.texture = self.ptexture 

        self.buftarget = "popup"
        self.tick_type = Object.TickTypes.PURGING

        #self.light_type = Object.LightTypes.DYNAMIC_TEXTURE_OVERLAY
        #self.light_texture = BGL.assets.get('NL-lights/texture/radial')
        #self.light_radius = 15
        self.lifespan = 90
        self.light_color = [ 1.0,0.7,0.0,0.0 ]
        self.color = [1.0,0.5,0.5,1.0]

        self.size = [ 3.8,3.8 ]
        if "ptexture" in self.__dict__:
            self.size = [ 5.0,5.0] 

        self.snapshot_fields = [ 'p' ]

        spd = 0.3 + uniform(0.2,0.8)
        self.vx = cos( self.rad )*spd
        self.vy = sin( self.rad )*spd
        self.rad = uniform(-3.14,3.14)

        
    def tick(self):
        self.color[3]*=0.95
        self.light_radius*=0.95
        self.vx*=0.9
        self.vy*=0.9
        self.vy+=0.02
        self.p[0] = self.p[0] + self.vx 
        self.p[1] = self.p[1] + self.vy 

        self.size[0]*=0.94
        self.size[1]*=0.94
        self.lifespan = self.lifespan-1
        if(self.lifespan<0):
            self.floor.objects.remove(self)
            return False
        return True
