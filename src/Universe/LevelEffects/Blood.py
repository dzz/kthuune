from Newfoundland.Object import Object
from random import choice, uniform
from Beagle import API as BGL

class Blood(Object):
    #texture = [
    #    BGL.assets.get("KT-forest/texture/blood0000"),
    #    BGL.assets.get("KT-forest/texture/blood0001"),
    #    BGL.assets.get("KT-forest/texture/blood0002"),
    #    BGL.assets.get("KT-forest/texture/blood0003"),
    #]
    texture = BGL.assets.get("KT-forest/animation/blood")

    def customize(self):
        self.rad = uniform(0.0,3.14*2)
        self.size = [ 3.0+uniform(0.0,1.0),3.0+uniform(0.0,1.0)]
        self.buftarget = "floor"
        self.tick_type = Object.TickTypes.STATIC
        self.texture = choice(Blood.texture)
        pass
