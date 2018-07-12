from Newfoundland.Object import Object
from Beagle import API as BGL
from math import floor
from ..RangedEnemyAttacks.BasicProjectile import BasicProjectile
from random import uniform

class DangerBlock(Object):
    textures = BGL.assets.get("KT-forest/animation/dangerblock")

    def customize(self):
        self.z_index = 1
        self.buftarget = "floor"
        self.tick_type = Object.TickTypes.TICK_FOREVER
        self.light_type = Object.LightTypes.NONE
        self.light_color = [0.0,1.0,1.0,1.0]
        self.light_radius = 1.5
        self.texture = DangerBlock.textures[0]
        self.size = [1.0,1.0]
        self.fire_rad = 0
        self.attack_str = 5
        self.timeout = 0
    
        self.fr = int(((self.p[0] * 4)+(self.p[1]*4))) % 66

    def tick(self):
        self.fr = self.fr + 1
        if(self.fr>= 100):
            self.fr = 0
        self.texture = DangerBlock.textures[self.fr//10]

        self.flash_color[3]*=0.94

        if(self.fr==29):
            self.flash_color = [ 1.0,0.4,1.0,1.0 ]
        if(self.fr==49):
            self.flash_color = [ 1.0,0.4,1.0,1.0 ]
        if(self.fr>=30) and (self.fr<=70):
            dx = self.p[0] - self.floor.player.p[0]
            dy = self.p[1] - self.floor.player.p[1]
            md = (dx*dx) + (dy*dy)

            if(self.timeout==0):
                if(md<3.5):
                    self.vx = uniform(-1.0,1.0)
                    self.vy = uniform(-1.0,1.0)
                    self.floor.player.receive_ranged_attack(self)
                    self.timeout = 4
            else:
                self.timeout-=1
        
        return True

    def parse(od,df):
        o = DangerBlock( p = [ od["x"], od["y"] ] )
        return o
