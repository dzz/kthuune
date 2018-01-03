from Newfoundland.Object import Object
from Beagle import API as BGL
from math import floor
from random import uniform

class Lantern(Object):
    def parse(od,df):
        return Lantern(p=[od["x"],od["y"]])

    def customize(self):
        self.buftarget = "popup"
        self.size = [ 1.0,1.0 ]
        self.light_color = [ 1.0,0.6,0.6,1.0 ]
        self.light_radius = 20
        self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
        self.visible = True
        self.textures = BGL.assets.get("KT-forest/animation/lantern")
        self.texture = self.textures[0]
        self.tick_type = Object.TickTypes.TICK_FOREVER
        self.z_index = 1
        self.fr = 0
        #self.physics = { "radius" : 1.0, "mass"   : 900, "friction" : 0.3 }

    def tick(self):
        self.light_color = [ uniform(0.7,1.0),uniform(0.3,0.6),0.2,1.0 ]
        self.light_radius = uniform(8.0,10.0)
        self.fr += 0.1
        if(self.fr>len(self.textures)):
            self.fr = 0.0
        self.texture = self.textures[floor(self.fr)]
        return True

    def get_shader_params(self):
        sp = Object.get_shader_params(self)
        return sp
