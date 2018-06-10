from Newfoundland.Object import Object
from Beagle import API as BGL
from random import uniform

class FireConcentrator(Object):
    texture = BGL.assets.get('KT-forest/texture/fireball')
    def customize(self):
        self.tick_type = Object.TickTypes.PURGING
        self.texture = FireConcentrator.texture
        self.size = [200.0,200.0]
        self.ttl = 90
        self.rp = uniform(-0.1,0.1)
        self.xp = uniform(0.9,0.98)
        self.light_type = Object.LightTypes.DYNAMIC_TEXTURE_OVERLAY
        self.visible = True
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
