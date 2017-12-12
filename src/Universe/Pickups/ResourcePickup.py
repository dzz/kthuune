from Newfoundland.Object import Object
from Beagle import API as BGL
from math import sin,cos,atan2
from ...KSounds import KSounds
from ...Abilities import Abilities
from random import choice

class ResourcePickup(Object):
    textures = [ 
        BGL.assets.get("KT-player/texture/thorium"),
        BGL.assets.get("KT-player/texture/neon"),
        BGL.assets.get("KT-player/texture/carbon"),
    ]
    names = [
        "Thorium",
        "Iridium",
        "Carbon"
    ]
   
    def customize(self):
        self.names = ResourcePickup.names
        self.fridx = 0
        self.pickup_type = choice([0,0,0,0,1,1,1,2,2])
        self.texture = ResourcePickup.textures[self.pickup_type]
        self.buftarget = "popup"
        self.base_p = list(self.p)
        self.tick_type = Object.TickTypes.PURGING
        self.light_type = Object.LightTypes.NONE
        self.light_color = [ 1.0, 1.0, 1.0, 1.0 ]
        self.light_radius = 1.0
        self.trigger_timer = 0
        self.visible = True

    def tick(self):
        self.trigger_timer = self.trigger_timer + 1
       
        if self.trigger_timer<30:
            return True 

        self.visible = True

        self.fridx = (self.fridx + 1) % 40
 
        y_offs = sin(self.fridx*(3.14/40.0))
        self.light_radius = 25. + y_offs

        self.p[1] = self.base_p[1] + (y_offs*0.15)

        dx = self.p[0] - self.floor.player.p[0]
        dy = self.p[1] - self.floor.player.p[1]

        md = (dx*dx) + (dy*dy)

        if (md<1.6):
            self.floor.objects.remove(self)
            self.floor.player.add_dm_message("You found some {0}".format(self.names[self.pickup_type]))

            if(self.pickup_type == 0):
                Abilities.ThoriumAmount += 1
            KSounds.play( KSounds.pickup )
            return False
        return True
