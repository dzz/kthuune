from Newfoundland.Object import Object
from Beagle import API as BGL

class SkullDeath(Object):
    texture = BGL.assets.get('KT-forest/texture/skull0000')

    def customize(self):
        self.texture = SkullDeath.texture
        self.buftarget = "hud"

        self.size =  [ 3.0, 3.0 ]
        self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
        self.light_color =  [ 1.0,0.0,1.0,1.0]
        self.color = [ 1.0,1.0,1.0,0.5]
        self.light_radius = 50.0
        self.physics = None
        self.z_index = 9000
        self.tick_type = Object.TickTypes.PURGING
        self.delta_vy = -0.03
        self.lifetime = 0
        self.delay = 0
        self.visible = False
        self.anim_tick = 0.2

    def tick(self):

        if(self.delay> 5):
            self.visible = True
            self.lifetime = self.lifetime + 1
            self.p[1] = self.p[1] + self.delta_vy
            self.delta_vy *= 1.1

            self.anim_tick = self.anim_tick * 1.08
            self.size[0] = sin( self.anim_tick ) * 5.0
            self.size[1] = self.size[1] * 1.02
            if(self.lifetime > 100):
                self.floor.objects.remove(self)
                return False
            return True
        else:
            self.delay = self.delay + 1
            return True
