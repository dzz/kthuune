from Newfoundland.Object import Object
from Beagle import API as BGL
from math import floor
from random import uniform

class Spawner(Object):
    textures = BGL.assets.get('KT-player/animation/explosion')

    def customize(self):
        sz = uniform(3.8,4.2)
        self.size = [ sz,sz]
        self.buftarget = "popup"
        self.tick_type = Object.TickTypes.PURGING
        self.texture = Spawner.textures[0]
        self.color = [ 0.0,0.0,1.0,1.0 ]
        self.fr = 0.0
        

    def spawn(self):
        new_object = self.loser.__class__( p = list(self.p) )
        self.floor.create_object( new_object )
        self.floor.snap_enemies.append( new_object )

    def tick(self):
        self.fr += 0.05

        self.color[0] = uniform(0.0,1.0)
        self.color[1] = uniform(0.0,1.0)
        self.color[2] = uniform(0.0,1.0)
        self.size[0]*=1.01
        self.size[1]*=1.01
        print(self.fr)
        if(self.fr>= len (Spawner.textures)):
            self.floor.remove_object(self)
            self.spawn()
            return False
        self.texture = Spawner.textures[floor(self.fr)]
        return True

