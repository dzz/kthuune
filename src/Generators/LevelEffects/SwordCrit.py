from Newfoundland.Object import Object
from Beagle import API as BGL

class SwordCrit(Object):
    texture = BGL.assets.get('KT-player/texture/sword')

    def customize(self):
        self.texture = SwordCrit.texture
        self.buftarget = "hud"

        self.size =  [ 9.0, 9.0 ]
        self.rad = 3.14/2
        #self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
        self.light_type = Object.LightTypes.NONE
        self.light_color =  [ 0.0,1.0,0.0,1.0]
        self.color = [ 1.0,1.0,1.0,0.5]
        self.light_radius = 50.0
        self.physics = None
        self.z_index = 9000
        self.tick_type = Object.TickTypes.PURGING
        self.delta_vy = 0.3
        self.lifetime = 0
        self.delay = 0
        self.visible = False
        self.anim_tick = 0.2

    def tick(self):

        if(self.delay> 5):
            self.visible = True
            self.lifetime = self.lifetime + 1
            self.p[1] = self.p[1] + self.delta_vy
            self.delta_vy *= 1.2

            self.anim_tick = self.anim_tick * 1.08
            if(self.lifetime > 30):
                self.floor.objects.remove(self)
                return False
            return True
        else:
            self.delay = self.delay + 1
            return True
