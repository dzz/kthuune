from Newfoundland.Object import Object
from math import sin,cos
from Beagle import API as BGL
from random import uniform, choice

class CrystalChunk(Object):
    textures = [
        BGL.assets.get('KT-forest/texture/crystal_1'),
        BGL.assets.get('KT-forest/texture/crystal_2'),
        BGL.assets.get('KT-forest/texture/crystal_3'),
        BGL.assets.get('KT-forest/texture/crystal_4')
    ]
    def __init__(self,**kwargs):
        Object.__init__(self,**kwargs)
        self.rad = uniform(-3.14,3.14)
        self.texture = choice(CrystalChunk.textures)
        self.buftarget = "popup"
        self.tick_type = Object.TickTypes.PURGING
        self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
        self.light_radius = 15
        self.lifespan = 90
        self.light_color = [ 1.0,0.7,0.0,0.0 ]
        self.color = [1.0,1.0,1.0,1.0]

        sz = uniform(2.0,4.0)
        self.size = [ sz,sz ]
        self.snapshot_fields = [ 'p' ]

        spd = 0.3 + uniform(0.2,0.8)
        self.vx = cos( self.rad )*spd
        self.vy = sin( self.rad )*spd
        self.rad = uniform(-3.14,3.14)

        
    def tick(self):
        self.color[3]*=uniform(0.98,0.999)
        self.light_radius*=0.95
        self.rad+=0.01
        self.vx*=0.9
        self.vy*=0.9
        self.vy+=0.02
        self.p[0] = self.p[0] + self.vx 
        self.p[1] = self.p[1] + self.vy 

        self.size[0]*=0.94
        self.size[1]*=0.94

        self.color[3]*=0.99
        self.lifespan = self.lifespan-1
        if(self.lifespan<0):
            self.floor.objects.remove(self)
            return False
        return True
