from Newfoundland.Object import Object
from Beagle import API as BGL
from math import sin,cos

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


    def fireRanged(self):
        print("KABOOM!")
        pass

    def tick(self):
        offs = 30

        pad = self.floor.player.controllers.get_virtualized_pad(self.floor.player.num)

        if(pad.triggers[0]+1.0<0.1) and self.fired:
            self.fired = False

        if(pad.triggers[1]>0.7) and (pad.triggers[0]+1.0>0.1):
            if not self.fired:
                self.fireRanged()
                self.fired = True


        self.size[1] = (pad.triggers[0]+1.0)*4.0;

        if(self.size[1] < 0.1):
            self.size[1] = 0.0

        if(self.fired):
            self.size[1] = 0.0

        print("fired?", self.fired)

        offsx = cos(self.floor.player.rad) * offs
        offsy = sin(self.floor.player.rad) * offs

        self.p[0] = self.floor.player.p[0] + offsx
        self.p[1] = self.floor.player.p[1] + offsy
        self.rad = self.floor.player.rad


