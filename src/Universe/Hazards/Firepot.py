from Newfoundland.Object import Object
from Beagle import API as BGL
from math import floor
from ..RangedEnemyAttacks.BasicProjectile import BasicProjectile
from random import uniform

class Firepot(Object):
    textures = [
        BGL.assets.get("KT-forest/texture/firepot0000"),
        BGL.assets.get("KT-forest/texture/firepot0001"),
        BGL.assets.get("KT-forest/texture/firepot0002"),
        BGL.assets.get("KT-forest/texture/firepot0003"),
        BGL.assets.get("KT-forest/texture/firepot0004"),
        BGL.assets.get("KT-forest/texture/firepot0005"),
    ]

    def customize(self):
        self.z_index = 1
        self.buftarget = "popup"
        self.tick_type = Object.TickTypes.TICK_FOREVER
        self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
        self.light_color = [0.0,1.0,1.0,1.0]
        self.light_radius = 1.5
        self.texture = Firepot.textures[0]
        self._fr = (0 - floor((self.p[1]+self.p[0])*3))%60
        self.size = [2.0,2.0]
        self.fire_rad = 0

    def tick(self):
        self._fr = (self._fr +1)%60
        self.texture = Firepot.textures[self._fr//10]
        self.light_radius *= 1.02
        if(self._fr == 50):
            self.light_radius = 1.5
            bolt = BasicProjectile( p = [ self.p[0], self.p[1] ], rad = self.fire_rad, animation = "orange" ) 
            self.floor.create_object( bolt )
            bolt.lifespan = 40
            bolt.rad += uniform(-0.04,0.04)

    def parse(od,df):
        o = Firepot( p = [ od["x"], od["y"] ] )
        return o
