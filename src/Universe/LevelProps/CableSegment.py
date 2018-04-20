from Newfoundland.Object import Object
from Beagle import API as BGL
from math import floor, atan2, hypot, sin, cos
from random import uniform, choice

class CableSegment(Object):
    regular = BGL.assets.get('KT-forest/animation/stainglass')

    def generate_cable( x1, y1, x2, y2):


        cum = [] 
        cur_x = x1
        cur_y = y1

        mag = 8.0
        nmag = 4.0
        smag = 5.0

        sfrq = 3.5 / 24.0

        sidx = uniform(0.0,3.2)

        while hypot(x2-cur_x, y1-cur_y)<2.0:
            nx1 =cur_x
            ny1 = cur_y

            dx = x2-nx1
            dy = y2-nx1

            l = hypot(dx,dy)

            dx/= l
            dy/= l

            nx2 = ((nx1 + (dx * mag)) + uniform(nmag,-nmag)) + (sin(sidx) * smag)
            ny2 = ((nx2 + (dy * mag)) + uniform(nmag,-nmag)) + (cos(sidx) * smag)

            mag /= 1.5
            nmag /= 1.7
            smag /= 2.2

            sfrq /= 1.3
            sidx += sfrq

            cum.append( CableSegment( x1 = cur_x, y1 = cur_y, x2 = nx2, y2=ny2 ) )
            cur_x = nx1
            cur_y = nx2

        return cum

        
    def customize(self):
        self.p = [
            (self.x1 + self.x2) / 2.0,
            (self.y1, + self.y2) / 2.0
        ]
        dx = self.x2 - self.x1
        dy = self.y2 - self.y1

        self.rad = atan2(dx,dy)

        self.size = [ hypot(dx,dy), uniform(1.0,2.0) ]

        #self.size = [ 3.0+uniform(0.0,1.0), 3.0+uniform(0.0,1.0) ]
        self.buftarget = "popup"
        self.tick_type = Object.TickTypes.STATIC
        self.texture = CableSegment.regular
        self.color = [ 1.0,1.0,1.0,1.0 ]
        self.fr = 0.0

