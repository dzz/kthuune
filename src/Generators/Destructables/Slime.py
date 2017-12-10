from Newfoundland.Object import Object
from .Breakable import Breakable
from Beagle import API as BGL
from math import sin,cos
from random import uniform, choice
from ..Particles.SplatterParticle import SplatterParticle
from ...KSounds import KSounds
from ..LevelEffects.Blood import Blood

class Slime(Breakable):
    def parse(od,df):
        ret = []
        for x in range(0,3):
            o = Slime( rad = uniform(0.0,6.5), p = [ od["x"], od["y"] ] )
            ret.append(o)
        return ret

    textures = [
        BGL.assets.get('KT-forest/texture/slime0small'),
        BGL.assets.get('KT-forest/texture/slime0big'),
    ]

    def customize(self):
        self.tick_type = Object.TickTypes.PURGING
        self.buftarget = "popup"
        self.visible = True
        self.texture = choice ( Slime.textures )
        sz = uniform(5.0,9.0)
        self._sz = sz
        self.size = [ sz*2.7,sz*2.7 ]
        self.base_size = [ self.size[0], self.size[1] ]
        self.physics = { "radius" : sz/3, "mass"   : 900000, "friction" : 0.3 }
        self.hitFr = 0
        self.hp = 2
        self.fridx = 0.0
        self.offs = uniform(0.0,3.14)
        self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
        self.light_radius = 30
        self.light_color = [ -0.3,0.3,-0.3,1.0]

    def tick(self):
        self.fridx += 0.01
        self.size[0] = (self.base_size[0] + (sin(self.fridx+self.offs)*2.0))*0.4
        self.size[1] = (self.base_size[1] + (cos(self.fridx+self.offs*0.8)*2.0))*0.4
        if self.hp>0:
            self.texture = Slime.textures[self.hp-1]
        if(self.hitFr>0):
            self.hitFr-=1
            self.rad+=uniform(-0.02,0.02)

        d = self.mdist( self.floor.player )

        if d < 90:
            self.floor.add_fog(self, 20.0 )
        if(self.hitFr==0):
            if self.floor.player.slash.visible:
                if d < self._sz*1.2:
                    #self.floor.player.add_dm_message("You hit a crystal with your sword")
                    for x in range(0,5):
                        self.floor.create_object( SplatterParticle( size = [ 5.0,5.0], ptexture = Slime.textures[0], rad=uniform(0.0,6.5), p = [ self.p[0], self.p[1]]))
                    KSounds.play(KSounds.slimecrush)
                    KSounds.play(KSounds.slashhit)
                    self.hitFr = 30
                    self.hp-=1

        if(self.hp==0):
            KSounds.play(KSounds.slimekill)
            self.handle_pull()
            self.floor.remove_object(self)

            #self.floor.player.add_dm_message("You smashed a crystal with your sword")
            #if uniform(0.0,1.0)>0.78:
            #    self.floor.create_object(ResourcePickup(p=[ self.p[0], self.p[1]]))
            
            for x in range(0,3):
                self.floor.create_object(Blood(p=[self.p[0]+uniform(-3.0,3.0),self.p[1]+uniform(-3.0,3.0)]))
            for x in range(0,15):
                self.floor.create_object( SplatterParticle( size = [ 5.0,5.0], ptexture = Slime.textures[0], rad= uniform(0.0,6.5), p = [ self.p[0], self.p[1]]))
            return False
        return True

    def get_shader_params(self):
        bp = Object.get_shader_params(self)

        if self.hitFr > 0:
            bp['translation_local'][0] += uniform(-0.01,0.01)
            bp['filter_color'] = [ 10.0,10.0,10.0,1.0]
        return bp
