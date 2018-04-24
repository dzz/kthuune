from Newfoundland.Object import Object
from Beagle import API as BGL
from math import floor, atan2, hypot, sin, cos, pi
from random import uniform, choice

class CablePin(Object):
    texture = BGL.assets.get('KT-forest/texture/registration')

    def customize(self):
        self.texture = CablePin.texture
        self.visible = True
        self.buftarget = "underfloor"
        self.size = [3.5,3.5]
        self.tick_type = Object.TickTypes.STATIC

class CableSegment(Object):
    texture = BGL.assets.get('KT-forest/texture/registration')
    next_x = 0.0
    wobble_idx = 0

    def generate_cable( x1, y1, x2, y2):
        print("GENERATING CABLE")

        cum = [] 
        cur_x = x1
        cur_y = y1

        dx = x2-x1
        dy = y2-y1
        l = hypot(dx,dy)

        dx/= l
        dy/= l

        max_seg = (floor(l / 4.0))+1
        mag = l / max_seg


        midx = 0.0
        mincr = pi / max_seg

        wt = 0.0
        wtincr = ((5+uniform(1.0,3.0))*pi) / max_seg

        for iter in range(0,max_seg-1):
    

            wmag = sin(midx)

            nx1 = cur_x
            ny1 = cur_y

            nx2 = nx1 + (mag*dx) + (sin(wt)*wmag) + (uniform(-wmag,wmag))
            ny2 = ny1 + (mag*dy) + (cos(wt)*wmag) + (uniform(-wmag,wmag))

            cur_x = nx2
            cur_y = ny2

            smod = ((sin(wt*0.5)*1.0)+2.0)*wmag

            cum.append( CableSegment( x1 = nx1, y1 = ny1, x2 = nx2, y2=ny2, smod=smod ) )

            dx = x2-nx2
            dy = y2-ny1
            l = hypot(dx,dy)

            dx/= l
            dy/= l

            max_seg -= 1
            mag = l / max_seg

            midx += mincr
            wt += wtincr


        cum.append(CablePin(p =[x1,y1]))
        cum.append(CablePin(p =[x2,y2]))
        return cum

        
    def tick(self):
        self.size[0] = self.basex * (1.0+(cos(self.w-self.p[0]-self.p[1])*0.08))
        self.size[1] = self.basey * (1.0+(sin(self.w+self.p[0]+self.p[1])*0.08))
        self.w += 0.02
        return True

    def customize(self):

        #self.p = [
        #    (self.x1 + self.x2) / 2.0,
        #    (self.y1 + self.y2) / 2.0
        #]

        self.p[0] = (self.x1 + self.x2) / 2.0
        self.p[1] = (self.y1 + self.y2) / 2.0

        dx = self.x2 - self.x1
        dy = self.y2 - self.y1

        self.rad = atan2(dy,dx) + uniform( pi/10.0, -1*(pi/10.0))

        self.size[0] = (hypot(dy,dx)/2.0) * 1.15
        self.size[1] = 1.0 + self.smod
        self.basex = self.size[0]
        self.basey = self.size[1]

        #self.size = [ 3.0+uniform(0.0,1.0), 3.0+uniform(0.0,1.0) ]
        self.buftarget = "underfloor"
        self.tick_type = Object.TickTypes.TICK_FOREVER
        self.texture = CableSegment.texture
        self.color = [ 1.0,1.0,1.0,1.0 ]
        self.fr = 0.0
        self.visible = True
        self.z_index = -9000
        self.w = CableSegment.wobble_idx
        CableSegment.wobble_idx += 0.2

