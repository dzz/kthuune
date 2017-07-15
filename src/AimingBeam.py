from Newfoundland.Object import Object
from Beagle import API as BGL
from math import sin,cos
from random import uniform as ur


class RangedMagic(Object):
    arrow_texture = BGL.assets.get("KT-player/texture/arrow")
    def __init__(self,**kwargs):
        Object.__init__(self,**kwargs)
        self.texture = RangedMagic.arrow_texture
        self.buftarget = "popup"
        self.tick_type = Object.TickTypes.PURGING
        self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
        self.light_radius = 5
        self.lifespan = 120
        self.light_color = [ 0.0,0.0,1.0,1.0 ]

        self.vx = cos( self.rad )*2
        self.vy = sin( self.rad )*2
        
    def tick(self):

        self.light_color[1] = ur(0.4,0.8)
        self.light_color[0] = ur(0.0,1.0)
        self.light_radius = ur(15,40)
        self.p[0] = self.p[0] + self.vx 
        self.p[1] = self.p[1] + self.vy 
        self.lifespan = self.lifespan - 1
        if(self.lifespan>0):
            return True
        self.floor.objects.remove(self)
        return False

class AimingBeam(Object):
    def __init__(self,**kwargs):
        Object.__init__(self,**kwargs)
        self.texture = BGL.assets.get("KT-player/texture/beam")
        self.tick_type = Object.TickTypes.TICK_FOREVER
        self.size = [30.0,1.0]
        self.light_type = Object.LightTypes.DYNAMIC_TEXTURE_OVERLAY
        self.visible = False
        self.buftarget = "popup"
        self.fired = False
        self.aiming = False

    def fireRanged(self):
        self.floor.create_object( RangedMagic( p = [ self.floor.player.p[0], self.floor.player.p[1] ], rad = self.floor.player.rad ) )
        print("KABOOM!")

    def tick(self):
        offs = 30

        pad = self.floor.player.controllers.get_virtualized_pad(self.floor.player.num)

        if(pad.triggers[0]+1.0<0.05) and self.fired:
            self.fired = False

        if(pad.triggers[1]>0.7) and (pad.triggers[0]+1.0>0.1):
            if not self.fired:
                self.fireRanged()
                self.fired = True


        self.size[1] = (pad.triggers[0]+1.0)*4.0;

        if(self.size[1] < 0.1):
            self.aiming = False
            self.size[1] = 0.0
        elif(self.fired):
            self.aiming = False
            self.size[1] = 0.0
        else:
            self.aiming = True

        #print("fired?", self.fired)
        #print("aiming?", self.aiming)
        offsx = cos(self.floor.player.rad) * offs
        offsy = sin(self.floor.player.rad) * offs

        self.p[0] = self.floor.player.p[0] + offsx
        self.p[1] = self.floor.player.p[1] + offsy
        self.rad = self.floor.player.rad


