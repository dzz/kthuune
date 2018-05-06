from Newfoundland.Object import Object
from Beagle import API as BGL
from math import sin,cos
from ..LevelProps.SpeechBubble import SpeechBubble
from random import choice
from math import floor

class Owl(Object):
    texture = BGL.assets.get('KT-forest/texture/owl')
    #texture = BGL.assets.get('KT-forest/texture/cave_entrance')

    def parse(od,df):
        o = Owl( p = [ od["x"], od["y"] ], group = od["meta"]["group"] )
        df.group_to_owl[od["meta"]["group"]]= o
        return o 

    def customize(self):
        self.texture = Owl.texture
        #self.buftarget = "popup"
        self.buftarget = "popup"
        self.size =  [ 7.0, 7.0 ]
        self.light_type = Object.LightTypes.DYNAMIC_TEXTURE_OVERLAY
        self.light_color =  [ 1.0,0.4,0.4,1.0]
        self._t = 0.0 
        self.physics = { "radius" : 2.0, "mass"   : 100.0, "friction" : 0.0 } 
        self.tick_type = Object.TickTypes.TICK_FOREVER
        self.z_index = 1

    def tick(self):
        self._t += 0.01
        self.rad = sin(self._t+(cos(self._t*1.0)*0.2)) * 0.15
        self.size[0] += (sin(self._t)*0.001)
        self.size[1] += (cos(self._t)*0.001)
        self.flash_color[3] *= 0.72
        return

