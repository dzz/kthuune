from Newfoundland.Object import Object
from Beagle import API as BGL
from math import floor, atan2, hypot, sin, cos
from random import uniform, choice

class CablePin(Object):
    texture = BGL.assets.get('KT-forest/texture/registration')

    def customize(self):
        self.texture = CablePin.texture
        self.visible = True
        self.buftarget = "popup"
        self.size = [3.5,3.5]
        self.tick_type = Object.TickTypes.STATIC

class CableSegment(Object):
    texture = BGL.assets.get('KT-forest/texture/registration')
    next_x = 0.0

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

        mag = l / 32

        for iter in range(0,32):

            nx1 = cur_x
            ny1 = cur_y

            nx2 = nx1 + (mag*dx)
            ny2 = ny1 + (mag*dy)

            cur_x = nx2
            cur_y = ny2

            cum.append( CableSegment( x1 = nx1, y1 = ny1, x2 = nx2, y2=ny2 ) )


        cum.append(CablePin(p =[x1,y1]))
        cum.append(CablePin(p =[x2,y2]))
        return cum

        
    def customize(self):


            
        print("SEGMENT....")
        print( self.x1, self.y1, self.x2, self.y2 )

        print("NUMERO UNO:")
        print(self.x1)
        print("END SEGMENT....")

        #self.p = [
        #    (self.x1 + self.x2) / 2.0,
        #    (self.y1 + self.y2) / 2.0
        #]

        self.p[0] = (self.x1 + self.x2) / 2.0
        self.p[1] = (self.y1 + self.y2) / 2.0

        dx = self.x2 - self.x1
        dy = self.y2 - self.y1

        self.rad = atan2(dy,dx)

        self.size[0] = hypot(dy,dx)/2.0
        self.size[1] = 1.0 

        #self.size = [ 3.0+uniform(0.0,1.0), 3.0+uniform(0.0,1.0) ]
        self.buftarget = "popup"
        self.tick_type = Object.TickTypes.STATIC
        self.texture = CableSegment.texture
        self.color = [ 1.0,1.0,1.0,1.0 ]
        self.fr = 0.0
        self.visible = True

