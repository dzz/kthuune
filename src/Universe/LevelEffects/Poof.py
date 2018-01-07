from Newfoundland.Object import Object
from Beagle import API as BGL
from math import floor
from random import uniform

class Poof(Object):
    textures = BGL.assets.get('KT-player/animation/explosion')

    def customize(self):
        sz = uniform(3.8,4.2)
        self.size = [ sz,sz]
        self.buftarget = "popup"
        self.tick_type = Object.TickTypes.PURGING
        self.texture = Poof.textures[0]
        self.color = [ 0.2,1.0,1.0,0.5 ]
        self.fr = 0.0

    def tick(self):
        self.fr += 0.2

        self.size[0]*=1.04
        self.size[1]*=1.04
        print(self.fr)
        if(self.fr>= len (Poof.textures)):
            self.floor.remove_object(self)
            return False
        self.texture = Poof.textures[floor(self.fr)]
        return True

