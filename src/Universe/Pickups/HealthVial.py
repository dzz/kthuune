from Newfoundland.Object import Object
from Beagle import API as BGL
from math import sin,cos,atan2
from ...KSounds import KSounds

class HealthVial(Object):
    textures = [ 
        BGL.assets.get("KT-player/texture/healthvial0000"),
        BGL.assets.get("KT-player/texture/healthvial0001"),
    ]
   
    def customize(self):
        self.fridx = 0
        self.texture = HealthVial.textures[0]
        self.buftarget = "popup"
        self.base_p = list(self.p)
        self.tick_type = Object.TickTypes.PURGING
        self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
        self.light_color = [ 1.0, 0.0, 0.0, 1.0 ]
        self.light_radius = 10.
        self.trigger_timer = 0
        self.visible = False

    def tick(self):
        self.trigger_timer = self.trigger_timer + 1
       
        if self.trigger_timer<30:
            return True 

        self.visible = True

        self.fridx = (self.fridx + 1) % 40
        self.texture = HealthVial.textures[int(self.fridx/20)]
 
        y_offs = sin(self.fridx*(6.28/40.0))

        self.rad = y_offs*0.1

        self.p[1] = self.base_p[1] + (y_offs*0.15)

        dx = self.p[0] - self.floor.player.p[0]
        dy = self.p[1] - self.floor.player.p[1]

        md = (dx*dx) + (dy*dy)

        if (md<2):
            if(self.floor.player.has_inv()):
                self.floor.objects.remove(self)
                self.floor.player.add_inv("hp_vial")
                KSounds.play( KSounds.pickup )
                return False

        return True
