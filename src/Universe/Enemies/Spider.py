from Newfoundland.Object import Object
from .SnapEnemy import SnapEnemy
from random import uniform, choice
from math import sin,cos,atan2,floor
from Beagle import API as BGL
from client.beagle.Newfoundland.GeometryUtils import segments_intersect
from ..LevelEffects.ChromaticWave import ChromaticWave
from ...KSounds import KSounds
from ..RangedEnemyAttacks.BasicProjectile import BasicProjectile

class Spider(SnapEnemy):
    def receive_snap_attack(self, was_crit):
        SnapEnemy.receive_snap_attack(self, was_crit)

    def parse(od,df):
        o = Spider( p = [ od["x"],od["y"] ] )
        SnapEnemy.set_group(o,od)
        df.snap_enemies.append(o)
        df.enemies.append(o)
        return o

    STATE_DEFAULT = 0

    textures = BGL.assets.get('KT-forest/animation/spider')
    def customize(self):

        self.op = list(self.p)
        self.triggered = False
        self.tick_type = Object.TickTypes.PURGING
        self.snap_type = SnapEnemy.ENEMY
        self.visible = True
        self.z_index = 1
        self.buftarget = "popup"
        self.texture = Spider.textures[0]
        self.widx = 0
        self.size = [ 2.2, 2.2 ]
        self.physics = { "radius" : 0.8, "mass"   : 0.0004, "friction" : 0.0 }
        self.state =  Spider.STATE_DEFAULT 
        self.stimer = 0

        self.snap_effect_emit = 0
        self.iframes = 0
        SnapEnemy.set_combat_vars(self)
        self.hp = 50
        

    def tick(self):

        #
        # this is noxious boilerplate
        #
        if(self.floor.player.title_card.displaying()):
            return True
        if(SnapEnemy.handle_tick_disabled(self)):
            return True
        if self.triggered:
            self.floor.add_fog(self, 0.30)

        SnapEnemy.tick(self)

        #
        # animation control... this is just something to start with or ignore
        #

        self.widx = (self.widx + 1) % (len(Spider.textures)*4)
        self.wfr = self.widx//4
        self.texture = Spider.textures[self.wfr]
        self.light_type = Object.LightTypes.NONE

        #
        # this is acrid boilerplate....
        #

        y = self.floor.player.p[0] - self.p[0]
        x = self.floor.player.p[1] - self.p[1]
        md = (x*x)+(y*y)
        if( md < 300 ):
            if not self.triggered:
                self.triggered = True
                test_segment = [ [ self.floor.player.p[0], self.floor.player.p[1] ], [self.p[0], self.p[1] ] ]
        if( md > 300 ):
            self.triggered = False

        if not self.triggered:
            if(self.hp < 0):
                SnapEnemy.die(self)
                return False
            return True

        self.visible = True


        ##########################################
        ##########################################
        ##########################################

        # go absolutely nuts here! refer to Acolyte, Celric, Skeline, Spawner...etc.... 
        
        self.stimer += 1
        if self.state == Spider.STATE_DEFAULT:
            pass
    
        ##########################################
        ##########################################
        ##########################################
        ##########################################

        
        if(self.hp < 0):
            SnapEnemy.die(self)
            return False

        return True

    def next_state( self, state ):
        self.stimer = 0
        self.state = state
    
    def get_shader_params(self):

        # this is how you adjust centering of a sprite to match the physics when the bitmap doesn't line up...

        bp = SnapEnemy.get_shader_params(self)
        bp['translation_local'][0] = 0.0
        bp['translation_local'][1] = -0.7
        return bp
