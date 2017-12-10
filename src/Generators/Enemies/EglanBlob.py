from Newfoundland.Object import Object
from .SnapEnemy import SnapEnemy
from random import uniform, choice
from math import sin,cos,atan2,floor
from Beagle import API as BGL
from client.beagle.Newfoundland.GeometryUtils import segments_intersect
from ..LevelEffects.ChromaticWave import ChromaticWave
from ...KSounds import KSounds
from ..RangedEnemyAttacks.BasicProjectile import BasicProjectile

class EglanBlob(SnapEnemy):

    def parse(od,df):
        eb = EglanBlob( p = [ od['x'],od['y'] ] )        
        df.snap_enemies.append(eb)
        return eb

    textures = [
        BGL.assets.get("KT-forest/texture/eglanblob1"),
        BGL.assets.get("KT-forest/texture/eglanblob2"),
        BGL.assets.get("KT-forest/texture/eglanblob3"),
        BGL.assets.get("KT-forest/texture/eglanblob4"),
        BGL.assets.get("KT-forest/texture/eglanblob5"),
        BGL.assets.get("KT-forest/texture/eglanblob6"),
        BGL.assets.get("KT-forest/texture/eglanblob7"),
    ] 

    def customize(self):
        self.snap_type = SnapEnemy.ENEMY
        self.triggered = False
        self.hp = 160
        self.dead = False
        self.tick_type = Object.TickTypes.PURGING
        self.physics = { "radius" : 0.5, "mass"   : 0.0003, "friction" : 1.0 }
        self.buftarget = "popup"
        self.visible = True
        self.texture = EglanBlob.textures[0]
        self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
        self.light_radius = 25
        self.defense = 1
        self.size = [ 7.0,7.0]
        self.iframes = 0
        self.fridx = uniform(0.0,100.0)
        self.snap_effect_emit = 0
        self.firing = False
        self.fire_idx = 0
        SnapEnemy.set_combat_vars(self)

    def fireRanged(self, rad):
        self.flash(1.0,0.8,0.0)
        #x = self.floor.player.p[0] - self.p[0]
        #y = self.floor.player.p[1] - self.p[1]
        #rad = atan2(y,x)
        self.floor.create_object( BasicProjectile( p = [ self.p[0], self.p[1] ], rad = rad ) )
        KSounds.play_eproj()

    def tick(self):
        self.fade_flash()
        SnapEnemy.tick(self)
        self.fridx += 1
        self.texture = EglanBlob.textures[ int(self.fridx/20) % 7 ]

        if(self.firing):
            self.fire_idx += 1
            if self.fire_idx % 12 == 0:
                rad = self.fire_base_rad
                rad += 0.3
                if(self.fire_idx>20):
                    self.fireRanged(rad)
                else:
                    self.flash_color = [ 0.0,0.0,0.0,1.0 ]
            if self.fire_idx > 90:
                self.firing = False
        else:
            self.fire_idx = 0
            self.fire_base_rad = uniform(-3.14,3.14)

        if self.texture == EglanBlob.textures[3]: 

            if(uniform(0.0,1.0)<0.01) and self.mdist(self.floor.player)<40:
                self.firing = True
            if choice([True,False,False]):
                self.v[0] = uniform(-8.0,8.0)
                self.v[1] = uniform(-8.0,8.0)
                if(self.v[1] >0 ):
                    self.size[0] = -7.0
                else:
                    self.size[0] = 7.0

        if self.texture == EglanBlob.textures[4]: 
            if choice([True,False,False]):
                dx = (self.floor.player.p[0] - self.p[0])
                dy = (self.floor.player.p[1] - self.p[1])
                self.v[0] = dx*0.25
                self.v[1] = dy*0.25

        self.light_color = [ abs(sin(self.fridx*0.03)),0.0,abs(cos(self.fridx*0.02)),1.0]

        if(self.hp < 0):
            SnapEnemy.die(self) #@bug physics not cleaned up
            return False
        return True

    def get_shader_params(self):
        sp = Object.get_shader_params(self)
        sp["translation_local"][1] += sin( self.fridx*0.03)*0.08
        return sp
