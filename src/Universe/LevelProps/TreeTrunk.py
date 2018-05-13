from Newfoundland.Object import Object
from Beagle import API as BGL
from random import choice,uniform
from math import sin,cos
from ..Particles.Bird import Bird

class TreeTrunk(Object):
    textures =[
         BGL.assets.get('KT-forest/texture/treetrunk'),
         BGL.assets.get('KT-forest/texture/shrub0000'),
         BGL.assets.get('KT-forest/texture/shrub0001'),
         BGL.assets.get('KT-forest/texture/shrub0002'),
         BGL.assets.get('KT-forest/texture/shrub0003')
    ]

    def tick(self):
        self.flash_color[3]*=0.93
        self.t += 0.011
        self.size[0] += (sin(self.t)) * 0.001

        if(self.t> self.bird_threshold):
            self.t = 0.0
            dx = self.floor.player.p[0] - self.p[0]
            dy = self.floor.player.p[1] - (self.p[1] + (self.size[1]))

            sd = abs(dx)+abs(dy)
            if(sd<20):
                self.flash_color = [ 1.0,1.0,1.0,1.0]
                for x in range(0,choice([3,5,7,10,20])):
                    spltr = Bird( p = [self.p[0]+uniform(0.0,self.size[0]), self.p[1]+uniform(-4.0,4.0)])
                    spltr.color = [0.0,0.0,0.0,1.0]
                    spltr.light_color = [ 0.0,1.0,0.0,1.0]
                    spltr.size[0]*=uniform(1.0,1.5)
                    self.floor.create_object(spltr)

    def parse(od,df):

        x1 = float(od["x"])
        y1 = float(od["y"])

        x2 = float(od["w"])
        y2 = float(od["h"])

        cx = (x1+x2) / 2.0
        cy = (y1+y2) / 2.0
      
        w = (x2-x1)*0.5
        h = (y2-y1)*0.5

        return TreeTrunk(
            bird_threshold=uniform(1.3,2.1),
            t=uniform(0.0,2.0),
            p=[cx,cy],
            size=[w,h],
            scale_uv=[1.0,1.0],
            tick_type = Object.TickTypes.TICK_FOREVER,
            visible = True,
            buftarget = "floor",
            texture = choice(TreeTrunk.textures)
            )
