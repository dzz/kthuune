from Newfoundland.Object import Object
from Beagle import API as BGL
from math import sin,cos,atan2
from ...KSounds import KSounds
from ...Abilities import Abilities

class SoftwarePickup(Object):
    textures = [ 
        BGL.assets.get("KT-player/texture/software"),
    ]
   
    def parse(od,df):
        o = SoftwarePickup( p = [ od["x"], od["y"] ], software_key = od["meta"]["key"] )
        return o
        
    def customize(self):
        self.fridx = 0
        self.texture = SoftwarePickup.textures[0]
        self.buftarget = "popup"
        self.base_p = list(self.p)
        self.tick_type = Object.TickTypes.PURGING
        self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
        self.light_color = [ 0.0, 1.0, 1.0, 1.0 ]
        self.light_radius = 25.
        self.visible = True
        self.size = [ 2.5,2.5 ]

        self.label = "UNKNOWN SOFTWARE"
        if self.software_key == "telekine":
            self.label = "TELEKINE BIOMETRICS"
        if self.software_key == "central":
            self.label = "CENTRAL PROCESSING"

    def tick(self):
        self.visible = True

        self.fridx = (self.fridx + 1) % 80
 
        y_offs = sin(self.fridx*(3.14/40.0))
        self.light_radius = 25. + y_offs

        self.size[0] = 2.5*y_offs
        self.p[1] = self.base_p[1] + (y_offs*0.15)

        md = self.mdist( self.floor.player )
        if (md<1.6):
            self.floor.objects.remove(self)
            KSounds.play( KSounds.pickup )
            self.floor.player.add_dm_message("You found a disk labelled: " + self.label)

            if self.software_key == "telekine":
                Abilities.InstallTelekine = True
            if self.software_key == "central":
                Abilities.InstallCentral = True
            return False
        return True
