from Newfoundland.Object import Object
from Beagle import API as BGL
from random import uniform
from math import sin,cos,atan2

class Firefly(Object):
    
    texture = BGL.assets.get('KT-player/texture/firefly')

    def __init__(self,**kwargs):
        self.flash_color = [ 1.0,1.0,0.0,1.0 ]
        Object.__init__(self,**kwargs)
        self.light_type = Object.LightTypes.DYNAMIC_TEXTURE_OVERLAY
        self.light_texture = BGL.assets.get('NL-lights/texture/radial')
        self.texture = Firefly.texture
        self.buftarget = "additive"
        self.is_pixie = False
        self.light_color = [ 1.0,0.6,0.3,1.0 ]
        self.color = [ 1.0,0.8,0.2,1.0]
        self.light_radius = 15
        self.tick_type = Object.TickTypes.PURGING
        self.life = 0
        self.trigger_life = uniform( 30.0,60.0 )
        self.base_p = self.p

        
        self.size = [0.7+uniform(0.0,0.3),0.7+uniform(0.0,0.3)]
        self.visible = True
        self.offs = uniform(0.0,3.14)

        spd = uniform(0.5,0.9)
        d = uniform(-3.14,3.14)
        self.vx = cos(d)*spd
        self.vy = sin(d)*spd

    def tick(self):
        self.flash_color[3]*=0.9
        self.life += 1

        self.p[0] = (self.p[0] *0.6) + (self.base_p[0]*0.4)
        self.p[1] = (self.p[1] *0.6) + (self.base_p[1]*0.4)
        self.p[0] = self.base_p[0]
        self.p[1] = self.base_p[1]

        if(self.life < self.trigger_life ):
            self.base_p[0] += self.vx
            self.base_p[1] += self.vy
        
            self.vx *= 0.93
            self.vy *= 0.97

            self.size[0]*=1.01
            self.size[1]*=1.01

            self.vx += sin(self.offs+(self.life*0.1))*0.03
            self.vy += cos(self.offs+(self.life*0.2))*0.03
        else:
            self.size[0]*=0.96
            self.size[1]*=0.96
            dx = self.floor.player.p[0] - self.base_p[0]
            dy = self.floor.player.p[1] - self.base_p[1]

            self.base_p[0] += dx/5.0
            self.base_p[1] += dy/5.0

            if self.mdist(self.floor.player)<1.0:
                self.floor.remove_object(self)
                if not self.is_pixie:
                    self.floor.player.add_firefly()
                    for x in range(0,3):
                        self.floor.create_object(PixieDust( p = [ self.p[0], self.p[1] ]))
                return False

        self.rad = atan2( self.vx, self.vy ) + (self.life/10.0)
        return True

class PixieDust(Firefly):
    def __init__(self,**kwargs):
        Firefly.__init__(self, **kwargs)
        self.texture = BGL.assets.get('NL-lights/texture/flare')
        self.color = [ 0.0,0.8,1.0,0.5]
        self.size[0] *=2
        self.size[1] *=2
        self.is_pixie = True
        spd = uniform(0.1,0.2)
        d = uniform(-3.14,3.14)
        self.vx = cos(d)*spd
        self.vy = sin(d)*spd
        self.trigger_life = uniform(20.0,30.0)
