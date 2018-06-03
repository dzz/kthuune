from Newfoundland.Object import Object
from random import choice, uniform
from Beagle import API as BGL

class PlayerPhantom(Object):
    def customize(self):
        self.texture = self.player.texture
        self.animation_target = ( self.target.p[0], self.target.p[1] )

        self.p[0] = self.player.p[0]
        self.p[1] = self.player.p[1]

        dx = self.animation_target[0] - self.p[0]
        dy = self.animation_target[1] - self.p[1]

        self.p[0] = self.p[0] - (dx*0.5)
        self.p[1] = self.p[1] - (dy*0.5)

        self.visible = False
        self.buftarget = "floor"
        self.z_index = 900
        self.tick_type = Object.TickTypes.PURGING
        self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
        self.light_radius = 20.0
        self.light_color = [ uniform(0.1,0.4),uniform(0.0,0.2),uniform(0.7,1.0),1.0 ]
        self.animation_counter = 0
        self.size = [ 6.7,6.7 ]

    
    def tick(self):
        self.light_radius *= 0.9
        self.animation_counter = self.animation_counter + 1
        if(self.animation_counter-self.animation_threshold > 12 ):
            self.floor.objects.remove(self)
            return False
        if(self.animation_counter > self.animation_threshold):
            self.visible = True
            dx = (self.animation_target[0] - self.p[0]) / 4
            dy = (self.animation_target[1] - self.p[1]) / 4
            self.p[0] = self.p[0] + dx
            self.p[1] = self.p[1] + dy
        return True
