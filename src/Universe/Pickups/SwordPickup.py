from Newfoundland.Object import Object
from Beagle import API as BGL
from math import sin,cos,atan2
from ...KSounds import KSounds
from ...Abilities import Abilities
from ..LevelProps.SpeechBubble import SpeechBubble

class SwordPickup(Object):
    textures = [ 
        BGL.assets.get("KT-player/texture/sword"),
    ]
   
    def parse(od,df):
        o = SwordPickup( p = [ od["x"], od["y"] ] )
        return o
        
    def customize(self):
        self.fridx = 0
        self.texture = SwordPickup.textures[0]
        self.buftarget = "popup"
        self.base_p = list(self.p)
        self.tick_type = Object.TickTypes.PURGING
        self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
        self.light_color = [ 0.0, 1.0, 1.0, 1.0 ]
        self.light_radius = 25.
        self.visible = True
        self.size = [ 2.5,2.5 ]
        self.rad = 3.14/2

    def tick(self):
        self.visible = True

        self.fridx = (self.fridx + 1) % 80
 
        y_offs = sin(self.fridx*(3.14/40.0))
        self.light_radius = 25. + y_offs

        self.size[1] = 2.5*y_offs
        self.p[1] = self.base_p[1] + (y_offs*0.15)

        dx = self.p[0] - self.floor.player.p[0]
        dy = self.p[1] - self.floor.player.p[1]

        md = (dx*dx) + (dy*dy)

        if (md<20):
            self.tooltip = 'a sword'
        if (md<1.6):
            sb = SpeechBubble( p = list(self.floor.player.p) )
            sb.trigger_script = [ "you've found a sword!", "push A to SLASH" ]
            sb.mode = 1
            self.floor.create_object( sb )
            self.floor.objects.remove(self)
            KSounds.play( KSounds.crit )
            self.floor.player.add_dm_message("You found a SWORD")

            self.floor.player.flash_color = [ 1.0,1.0,1.0,1.0]
            Abilities.Sword = True

            return False
        return True
