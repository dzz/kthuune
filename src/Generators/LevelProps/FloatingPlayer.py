from Newfoundland.Object import Object
from Beagle import API as BGL
from random import uniform, choice
from math import sin,cos

class FloatingPlayer(Object):
    def parse(od,df):
        FloatingPlayer.instance = FloatingPlayer(p=[od["x"],od["y"]])
        return FloatingPlayer.instance

    def customize(self):
        self.buftarget = "floor"
        self.tick_type = Object.TickTypes.PURGING
        self.visible = True
        self.fr = 0
        self.fridx = 0.0
        self.texture = BGL.assets.get('KT-player/texture/knight0018')
        self.size = [ 2.0,2.0 ]
        self.color = [ 0.0,1.0,0.0,0.7 ]
        self.base_p = list(self.p)
        self.z_index = 9000

    def tick(self):
        self.fridx += 1.0
        if not self.floor.player.title_card.displaying():
            self.fr += 1
            self.p[0] = float(self.base_p[0] + uniform(-0.5,0.5)*(self.fr/80))
        #self.p[1] = float(self.base_p[1] + (sin(self.fridx/20)*0.7))

        offs = sin(self.fridx/20)*0.5
        self.p[1] = float(self.base_p[1])+offs

        if(self.fr<80):
            return True
        return False
    
