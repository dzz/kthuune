from Newfoundland.Object import Object
from Beagle import API as BGL
from random import uniform

class ChromaticWave(Object):
    texture = BGL.assets.get('NL-lights/texture/flare')
    def customize(self):
        self.tick_type = Object.TickTypes.PURGING
        self.texture = ChromaticWave.texture
        self.size = [0.1,0.1]
        self.ttl = 90
        self.rp = uniform(-0.1,0.1)
        self.xp = uniform(1.01,1.08)
        self.light_type = Object.LightTypes.DYNAMIC_TEXTURE_OVERLAY
        self.visible = False
        self.buftarget = "floor"
        self.z_index = 100

    def tick(self):
        #self.light_color[3] = self.light_color[3] * uniform(0.7,0.9)
        #self.color[3] = self.color[3] * uniform(0.7,0.9)
        self.rad = self.rad + self.rp
        self.light_radius = uniform(10.0,80.0)

        self.size[0] = self.size[0]*self.xp
        self.size[1] = self.size[1]*self.xp
        self.ttl = self.ttl - 1
        if(self.ttl<0):
            self.floor.objects.remove(self)
            return False

        return True
