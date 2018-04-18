from Newfoundland.Object import Object
from Beagle import API as BGL
from math import floor
from random import uniform, choice

class Stainglass(Object):
    regular = BGL.assets.get('KT-forest/animation/stainglass')
    tulip = BGL.assets.get('KT-forest/animation/tulipglass')

    def parse(od,df):
        o = Stainglass( p = [ od["x"],od["y"] ] )
        return o
        
    def customize(self):
        self.size = [ 3.0+uniform(0.0,1.0), 3.0+uniform(0.0,1.0) ]
        self.buftarget = "popup"
        self.tick_type = Object.TickTypes.PURGING
        self.textures = choice([Stainglass.regular, Stainglass.tulip ])
        self.texture = self.textures[0]
        self.color = [ 1.0,1.0,1.0,1.0 ]
        self.fr = 0.0

    def tick(self):
        self.fr += 0.05

        if(self.fr>= len (self.textures)):
            self.fr = 0
        self.texture = self.textures[floor(self.fr)]

        return True

