from Newfoundland.Object import Object
from Beagle import API as BGL
from math import floor
from random import uniform

class Dust(Object):
    textures = BGL.assets.get('KT-player/animation/dust')

    def customize(self):

        sz = uniform(0.8,1.1)
        self.size = [ sz,sz]
        self.buftarget = "floor"
        self.tick_type = Object.TickTypes.PURGING
        self.texture = Dust.textures[0]
        self.color = [ 1.0,1.0,1.0,uniform(0.7,0.9)]
        self.fr = 0.0

    def tick(self):
        self.fr += 0.2
        if(self.fr>= len (Dust.textures)):
            self.floor.remove_object(self)
            return False
        self.texture = Dust.textures[floor(self.fr)]
        return True

