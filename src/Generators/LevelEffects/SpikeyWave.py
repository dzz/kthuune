from Newfoundland.Object import Object
from Beagle import API as BGL
from random import uniform
from math import floor

class SpikeyWave(Object):
    textures = [
        BGL.assets.get('KT-forest/texture/splat0000'),
        BGL.assets.get('KT-forest/texture/splat0001'),
        BGL.assets.get('KT-forest/texture/splat0002'),
        BGL.assets.get('KT-forest/texture/splat0003'),
    ]
    def customize(self):
        self.tick_type = Object.TickTypes.PURGING
        self.cooldown = 80
        self.rad = uniform(-3.14,3.14)
        self.buftarget = "popup"
        self.zindex = 100
        self.size = [ uniform(1.3,2.7), uniform(1.3,2.7) ]
        self.spin = uniform(-0.1,0.1)

    def get_shader_params(self):
        sp = Object.get_shader_params(self)
        sp["filter_color"] = [1.0,1.0,1.0,float(self.cooldown)/80.]
        return sp

    def tick(self):
        self.floor.add_fog( self, 0.1 )
        self.size[0] = self.size[0] * 1.2 
        self.size[1] = self.size[1] * 1.2 
        self.rad = self.rad + self.spin
        self.cooldown = self.cooldown - 4.0
        if(self.cooldown<=0):
            self.floor.objects.remove(self)
            return False
        else:
            self.texture = SpikeyWave.textures[int(floor((80-self.cooldown) / 80)) ]
            return True
