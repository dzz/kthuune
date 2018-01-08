from Newfoundland.Object import Object
from Beagle import API as BGL
from math import floor
from random import uniform

from ..LevelEffects.Poof import Poof
from ..LevelEffects.AttackInfo import AttackInfo

class Hostage(Object):
    textures = BGL.assets.get('KT-forest/animation/hostage')

    def parse(od,df):
        o = Hostage( p = [ od["x"],od["y"] ] )
        df.hostages.append(o)
        return o
        
    def customize(self):
        sz = uniform(1.8,2.2)
        self.size = [ sz,sz]
        self.buftarget = "popup"
        self.tick_type = Object.TickTypes.PURGING
        self.texture = Hostage.textures[0]
        self.color = [ 1.0,1.0,1.0,1.0 ]
        self.fr = 0.0

    def tick(self):
        self.fr += 0.1

        if uniform(0.0,1.0)>0.99:
            self.size[0] *= -1

        if(self.fr>= len (Hostage.textures)):
            self.fr = 0
        self.texture = Hostage.textures[floor(self.fr)]

        if(self.mdist( self.floor.player)<2):
            self.floor.create_object(Poof( p = list(self.p)))
            self.floor.objects.remove(self)
            self.floor.create_object(AttackInfo( p=[ self.p[0], self.p[1] ], message="HOSTAGE RESCUED!"))
            return False            
        return True

