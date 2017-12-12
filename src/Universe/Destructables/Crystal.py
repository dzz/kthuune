from Newfoundland.Object import Object
from .Breakable import Breakable
from Beagle import API as BGL
from math import sin,cos
from random import uniform, choice
from ..Particles.CrystalChunk import CrystalChunk
from ...KSounds import KSounds
from ..Pickups.ResourcePickup import ResourcePickup
from random import choice

class Crystal(Breakable):
    def parse(od,df):
        ret = []
        for x in range(0,3):
            o = Crystal( rad = uniform(0.0,6.5), p = [ od["x"], od["y"] ] )
            ret.append(o)
        return ret

    textures = [
        BGL.assets.get('KT-forest/texture/crystal_1'),
        BGL.assets.get('KT-forest/texture/crystal_2'),
        BGL.assets.get('KT-forest/texture/crystal_3'),
        BGL.assets.get('KT-forest/texture/crystal_4')
    ]

    def customize(self):
        self.tick_type = Object.TickTypes.PURGING
        self.buftarget = "popup"
        self.visible = True
        self.texture = choice ( Crystal.textures )
        sz = uniform(4.0,8.0)
        self._sz = sz
        self.size = [ sz*0.7,sz*0.7 ]
        self.physics = { "radius" : sz/3, "mass"   : 900000, "friction" : 0.3 }
        self.hitFr = 0
        self.hp = choice([1,1,2])

    def tick(self):

        if(self.hitFr>0):
            self.hitFr-=1
            self.rad+=uniform(-0.02,0.02)

        if(self.hitFr==0):
            if self.floor.player.slash.visible:
                d = self.mdist( self.floor.player )
                if d < self._sz*1.2:
                    #self.floor.player.add_dm_message("You hit a crystal with your sword")
                    for x in range(0,5):
                        self.floor.create_object( CrystalChunk( p = [ self.p[0], self.p[1]]))
                    KSounds.play(KSounds.mining1)
                    self.hitFr = 30
                    self.hp-=1

        if(self.hp==0):
            KSounds.play(KSounds.mining2)
            self.handle_pull()
            self.floor.remove_object(self)

            #self.floor.player.add_dm_message("You smashed a crystal with your sword")
            if uniform(0.0,1.0)>0.78:
                self.floor.create_object(ResourcePickup(p=[ self.p[0], self.p[1]]))
            
            for x in range(0,15):
                self.floor.create_object( CrystalChunk( p = [ self.p[0], self.p[1]]))
            return False
        return True

    def get_shader_params(self):
        bp = Object.get_shader_params(self)

        if self.hitFr > 0:
            bp['translation_local'][0] += uniform(-0.2,0.2)
            bp['filter_color'] = [ 10.0,10.0,10.0,1.0]
        return bp
