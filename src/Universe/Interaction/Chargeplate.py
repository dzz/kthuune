from Newfoundland.Object import Object
from Beagle import API as BGL
from math import floor
from random import uniform

from ..LevelEffects.Poof import Poof
from ..LevelEffects.AttackInfo import AttackInfo

class Chargeplate(Object):
    textures = BGL.assets.get('KT-forest/animation/chargeplate')

    def parse(od,df):
        o = Chargeplate( p = [ od["x"],od["y"] ] )
        return o
        
    def customize(self):
        self.size = [ 2.0, 2.0 ]
        self.buftarget = "floor"
        self.tick_type = Object.TickTypes.PURGING
        self.texture = Chargeplate.textures[0]
        self.color = [ 0.0,0.0,0.0,1.0 ]
        self.fr = 0.0
        self.cv = 0.0
        self.charged = False

    def tick(self):

        if(self.charged):
            self.texture = Chargeplate.textures[ len(Chargeplate.textures)-1]
            self.color = [ 1.0,1.0,1.0,1.0 ]
            win = True
            for cp in self.floor.chargeplates:
                if(not cp.charged):
                    win = False
                    break                    
            if win: 
                dfloor = self.floor
                def ns():
                    dfloor.game.next_sequence()
                self.floor.add_timeout( [ ns, 120 ] )
            return False

        self.fr += self.cv

        if(self.fr>= len (Chargeplate.textures)):
            self.fr = 0
        self.texture = Chargeplate.textures[floor(self.fr)]

        if(self.mdist( self.floor.player)<2):
            self.cv += 0.01
            #self.floor.create_object(Poof( p = list(self.p)))
            #self.floor.objects.remove(self)
            #return False            
        else:
            self.cv *= 0.98

        if(self.cv>1.0):
            self.cv = 1.0
            self.charged = True
            self.floor.create_object(AttackInfo( p=[ self.p[0], self.p[1] ], message="CHARGED!"))

        self.color = [
            self.cv,
            self.cv,
            1.0,
            1.0 ]
        return True

