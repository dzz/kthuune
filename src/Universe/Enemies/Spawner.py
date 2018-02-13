from Newfoundland.Object import Object
from Beagle import API as BGL
from math import floor
from random import uniform, choice
from ..LevelEffects.AttackInfo import AttackInfo

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
        self.fv = uniform(0.03,0.08)
        

    def spawn(self):
        self.floor.create_object(AttackInfo( p=[ self.p[0], self.p[1] ], message="~respawn~"))
        self.floor.sounds.play(self.floor.sounds.spawned)
        new_object = self.loser.__class__( p = list(self.p) )
        new_object.group = self.loser.group
        new_object.group_active = self.loser.group_active
        new_object.flash_color = [ 0.0,1.0,0.0,1.0 ]
        self.floor.create_object( new_object )
        self.floor.snap_enemies.append( new_object )
        self.floor.enemies.append( new_object )

    def tick(self):

        if(self.floor.playing_genocide()):
            if not self.floor.passed_genocide:
                self.spawn()
            self.floor.remove_object(self)
            return False

        self.fr += self.fv

        self.color[0] = uniform(0.0,1.0)
        self.color[1] = uniform(0.0,1.0)
        self.color[2] = uniform(0.0,1.0)
        self.size[0]*=1.01
        self.size[1]*=1.01
        if(self.fr>= len (Spawner.textures)):
            self.floor.remove_object(self)
            self.spawn()
            return False
        self.texture = Spawner.textures[floor(self.fr)]
        return True

