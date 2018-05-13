from Newfoundland.Object import Object
from random import choice, uniform
from Beagle import API as BGL
from math import sin,cos,floor

class Bird(Object):
    texture = BGL.assets.get('KT-forest/animation/bird')
    def __init__(self,**kwargs):
        Object.__init__(self,**kwargs)

        self.buftarget = "popup"
        self.tick_type = Object.TickTypes.PURGING

        #self.light_type = Object.LightTypes.DYNAMIC_TEXTURE_OVERLAY
        #self.light_texture = BGL.assets.get('NL-lights/texture/radial')
        #self.light_radius = 15
        self.lifespan = 150
        self.light_color = [ 1.0,0.7,0.0,0.0 ]
        self.color = [1.0,0.5,0.5,1.0]
        self.fr = 0

        sz = uniform(0.3,0.5)
        self.size = [ sz, sz ]

        self.snapshot_fields = [ 'p' ]

        self.rad = uniform(-0.8,0.8)
        self.vx = uniform(-1.0,1.0)
        self.vy = uniform(-0.5,-1.5)

        if(self.vx>0):
            self.size[0]*=-1

        self.delay = uniform(10.0,90.0)
        self.visible = False
        self.z_index = 9000000
        self.rad = uniform(-0.2,0.2)

        
    def tick(self):
        self.size[0] *= 1.01
        self.size[1] *= 1.015
        self.fr += 1
        if self.fr<self.delay:
            self.flash_color = [ 1.0,1.0,1.0,1.0 ]
            return True

        self.flash_color[3]*=0.9
        self.color[3] *= 0.99
        self.visible = True
        self.texture = Bird.texture[floor(self.fr/10)%len(Bird.texture)]
        self.light_radius*=0.95
        self.vx*=1.09
        self.vy*=1.03
        self.vy-=0.01

        self.vx += sin(self.vy*0.1)*0.01

        self.p[0] = self.p[0] + (self.vx *0.04)
        self.p[1] = self.p[1] + (self.vy *0.04)

        #self.size[0]*=0.94
        #self.size[1]*=0.94

        self.lifespan = self.lifespan-1
        if(self.lifespan<0):
            self.floor.objects.remove(self)
            return False
        return True
