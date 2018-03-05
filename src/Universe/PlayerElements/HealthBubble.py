from Beagle import API as BGL
from Newfoundland.Object import Object
from random import uniform

class HealthBubble(Object):
    texture = BGL.assets.get("KT-player/texture/flare")
    def __init__(self,**kwargs):
        Object.__init__(self,**kwargs)
        self.texture = HealthBubble.texture
        self.buftarget = "popup"
        self.tick_type = Object.TickTypes.PURGING
        self.light_type = Object.LightTypes.NONE

        if(uniform(0.0,1.0)>0.8):
            self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
        self.light_radius = 5
        self.lifespan = 1390
        self.light_color = [ 1.0,0.0,0.0,0.0 ]
        self.color = [1.0,0.0,0.0,1.0]

        self.size = [ 2.8,2.8 ]
        self.snapshot_fields = [ 'p' ]

        self.vx = uniform(-0.05,0.05)
        self.vy = uniform(-0.1,-0.2)

    def tick(self):
        self.color[3]*=uniform(0.98,0.999)
        self.light_radius*=0.99
        self.vx*=0.99
        self.p[0] = self.p[0] + self.vx 
        self.p[1] = self.p[1] + self.vy 

        #self.size[0]*=0.99
        #self.size[1]*=0.99
        self.lifespan = self.lifespan-1
        if(self.lifespan<0):
            self.floor.objects.remove(self)
            return False
        return True
