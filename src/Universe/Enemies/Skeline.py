from Newfoundland.Object import Object
from .SnapEnemy import SnapEnemy
from random import uniform, choice
from math import sin,cos,atan2,floor
from Beagle import API as BGL
from client.beagle.Newfoundland.GeometryUtils import segments_intersect
from ..LevelEffects.ChromaticWave import ChromaticWave
from ...KSounds import KSounds
from ..RangedEnemyAttacks.BasicProjectile import BasicProjectile

class Skeline(SnapEnemy):
    def receive_snap_attack(self, was_crit):
        SnapEnemy.receive_snap_attack(self, was_crit)
        self.stimer = -10
        self.state = Skeline.STATE_SEEKING_RANDOM

    def parse(od,df):
        o = Skeline( p = [ od["x"],od["y"] ] )
        df.snap_enemies.append(o)
        return o

    STATE_SEEKING_RANDOM = 0
    STATE_SEEKING_PLAYER = 1
    STATE_CHARGING_SHOT = 2
    STATE_FIRING_SHOT = 3

    textures = [
        BGL.assets.get("KT-forest/texture/skeline0000"),
        BGL.assets.get("KT-forest/texture/skeline0001"),
        BGL.assets.get("KT-forest/texture/skeline0002"),
        BGL.assets.get("KT-forest/texture/skeline0003"),
    ] 
    def customize(self):
        self.triggered = False
        self.tick_type = Object.TickTypes.PURGING
        self.snap_type = SnapEnemy.ENEMY
        self.visible = True
        self.z_index = 1
        self.buftarget = "popup"
        self.texture = Skeline.textures[0]
        self.widx = int(uniform(0.0,40.0))
        self.size = [ 2.5, 2.5 ]
        self.physics = { "radius" : 0.35, "mass"   : 0.0005, "friction" : 0.0 }
        self.state = choice( [ Skeline.STATE_SEEKING_RANDOM, Skeline.STATE_SEEKING_PLAYER ] )
        #self.state = Skeline.STATE_SEEKING_RANDOM
        self.stimer = 0
        self.rvx = None
        self.speed = 3.8
        self.invert_seek = False
        self.flip_pxy = False

        self.snap_effect_emit = 0
        self.iframes = 0
        SnapEnemy.set_combat_vars(self)
        self.hp = 50
        

    def tick(self):
        if self.triggered:
            self.floor.add_fog(self, 0.30)
        SnapEnemy.tick(self)
        self.widx = (self.widx + 1) % 40
        self.wfr = floor(self.widx/20)
        self.texture = Skeline.textures[self.wfr]
        self.light_type = Object.LightTypes.NONE

        y = self.floor.player.p[0] - self.p[0]
        x = self.floor.player.p[1] - self.p[1]

        md = (x*x)+(y*y)
        if( md < 300 ):
            if not self.triggered:
                self.triggered = True
                test_segment = [ [ self.floor.player.p[0], self.floor.player.p[1] ], [self.p[0], self.p[1] ] ]
                for segment in self.floor.get_light_occluders():
                    if segments_intersect( segment, test_segment ):
                        self.triggered = False
                        break 
        if( md > 300 ):
            self.triggered = False

        if not self.triggered:
            if(self.hp < 0):
                SnapEnemy.die(self)
                return False
            #self.visible = False
            return True

        self.visible = True

        self.stimer = self.stimer + 1

        if self.invert_seek:
            calc_speed = self.speed * -0.4
        else:
            calc_speed = self.speed * 1.2

        if self.state == Skeline.STATE_SEEKING_PLAYER:

            ### hack acolyte seek
            p = self.floor.player.p
            pscore = abs(p[0] - self.p[0]) + abs(p[1]-self.p[1])
            for enemy in self.floor.snap_enemies:
                if not self.invert_seek and "is_acolyte" in enemy.__dict__ and enemy.triggered:
                    apscore = abs(enemy.p[0] - self.p[0]) + abs(enemy.p[1]-self.p[1])
                    if apscore<pscore:
                        p=enemy.p
                        break
        
                        

            self.rvx = None
            if self.flip_pxy:
                y = p[0] - self.p[0]
                x = p[1] - self.p[1]
            else:
                x = p[0] - self.p[0]
                y = p[1] - self.p[1]
    


            rad = atan2(y,x)
            vx = cos(rad) * calc_speed
            vy = sin(rad) * calc_speed
            self.v = [ vx,vy]

            if(self.stimer > 12 ):
                self.stimer = 0
                self.state = choice( [ Skeline.STATE_SEEKING_RANDOM, Skeline.STATE_SEEKING_PLAYER, Skeline.STATE_SEEKING_PLAYER ] )
                self.invert_seek = choice( [ False, True, False ] )
                if( self.state == Skeline.STATE_SEEKING_RANDOM ):
                    self.state = choice( [ Skeline.STATE_SEEKING_RANDOM, Skeline.STATE_CHARGING_SHOT, Skeline.STATE_SEEKING_PLAYER ] )
                    self.flip_pxy = choice( [ True, True, True, False ] )
        if self.state == Skeline.STATE_SEEKING_RANDOM:
            if not self.rvx:
                self.rvx = [ uniform(-1.0,1.0), uniform(-1.0,1.0) ]
                self.flip_pxy = choice( [ True, False ] )
            self.v = [ self.rvx[0] * calc_speed, self.rvx[1] * calc_speed ]
            if(self.stimer > 5 ):
                self.stimer = 0
                self.state = choice( [ Skeline.STATE_SEEKING_RANDOM, Skeline.STATE_SEEKING_PLAYER, Skeline.STATE_CHARGING_SHOT ] )
                self.invert_seek = choice( [ True, False ] )
        if self.state == Skeline.STATE_CHARGING_SHOT:
            if(self.stimer==1):
                KSounds.play(KSounds.charging_projectile)
            self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
            self.light_color = [1.0,0.4,0.1,1.0]
            self.light_radius = uniform(10.0,20.0)
            self.v = [0.0,0.0]
            self.texture = Skeline.textures[2]
            self.floor.create_object( ChromaticWave( p = [ self.p[0], self.p[1] ] ) )
            if( self.stimer > 20 ):
                self.stimer = 0
                self.state = Skeline.STATE_FIRING_SHOT
                self.pickTarget()
        if self.state == Skeline.STATE_FIRING_SHOT:
            self.texture = Skeline.textures[3]
            if( self.stimer > 15 ):
                self.state = Skeline.STATE_SEEKING_PLAYER
                self.fireRanged()

        if(self.hp < 0):
            SnapEnemy.die(self)
            return False

        return True

    def pickTarget(self):
        x = (self.floor.player.p[0] - self.p[0])+self.floor.player.v[0]
        y = (self.floor.player.p[1] - self.p[1])+self.floor.player.v[1]
        rad = atan2(y,x)
        self.target_rad = rad
        
    def fireRanged(self):
        self.flash(1.0,0.8,0.0)
        #x = self.floor.player.p[0] - self.p[0]
        #y = self.floor.player.p[1] - self.p[1]
        #rad = atan2(y,x)
        self.floor.create_object( BasicProjectile( p = [ self.p[0], self.p[1] ], rad = self.target_rad ) )
        KSounds.play_eproj()

    def get_shader_params(self):
        bp = SnapEnemy.get_shader_params(self)
        bp['translation_local'][0] = 0.1
        bp['translation_local'][1] = -0.4
        return bp
