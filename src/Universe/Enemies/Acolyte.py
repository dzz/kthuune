from Newfoundland.Object import Object
from .SnapEnemy import SnapEnemy
from random import uniform, choice
from math import sin,cos,atan2,floor
from Beagle import API as BGL
from client.beagle.Newfoundland.GeometryUtils import segments_intersect
from ..LevelEffects.ChromaticWave import ChromaticWave
from ...KSounds import KSounds
from ..RangedEnemyAttacks.BasicProjectile import BasicProjectile
from .Skeline import Skeline #TODO: eliminate this dependency
from ..Hazards.WormField import WormField
from ..LevelEffects.AttackInfo import AttackInfo
from ..Particles.SplatterParticle import SplatterParticle
from ..LevelEffects.Explosion import Explosion

class Acolyte(SnapEnemy):
    def custom_die(self):
        #for enemy in self.floor.snap_enemies:
        #    if enemy.snap_type == SnapEnemy.ENEMY:
        #        if enemy.triggered:
        #            enemy.receive_snap_attack(True)

        notify_timeout = 20
        if(self.floor.playing_genocide()):
            target_group = self.group+1
            for enemy in self.floor.enemies:
                #print("CHECKING ENEMEY GROUP {0} == {1}",enemy.group, target_group )
                if enemy.group == target_group and enemy.hp>0 and enemy.group_active == False:
                    def fes(enemy):
                        def es():
                            enemy.group_active = True
                            enemy.flash_color = [ 1.0,1.0,1.0, 1.0 ]
                            enemy.p[0] += 99999
                            enemy.p[1] += 99999
                            enemy.physics_suspended = False
                            enemy.tick()
                            enemy.visible = True
                            enemy.triggered = True
                            ai= AttackInfo( p=[ enemy.p[0], enemy.p[1] ], message="~infection~")
                            self.floor.create_object( Explosion( p = list(enemy.p) ) )
                            self.floor.create_object(ai)
                            self.floor.camera.grab_cinematic( ai, 50 )
                            self.floor.sounds.play(self.floor.sounds.spawned)
                        return es

                    self.floor.add_timeout( [fes(enemy), notify_timeout])
                    notify_timeout += 50
                    

        def mk_wormfield():
            wf_spec = [ self.p[0], self.p[1], 15 ]
            self.floor.create_object( WormField( wf_spec = wf_spec) )
        self.floor.add_timeout( [ mk_wormfield , notify_timeout ] )

    def receive_snap_attack(self, was_crit):
        SnapEnemy.receive_snap_attack(self, was_crit)
        self.stimer = 0
        self.state = Acolyte.STATE_CHARGING_SHOT

    def parse(od,df):
        o = Acolyte( p = [ od["x"],od["y"] ] )
        SnapEnemy.set_group(o,od)
        df.snap_enemies.append(o)
        df.enemies.append(o)
        return o

    STATE_SEEKING_RANDOM = 0
    STATE_SEEKING_PLAYER = 1
    STATE_CHARGING_SHOT = 2
    STATE_FIRING_SHOT = 3

    textures = [
        BGL.assets.get("KT-forest/texture/acolyte0000"),
        BGL.assets.get("KT-forest/texture/acolyte0001"),
        BGL.assets.get("KT-forest/texture/acolyte0002")
    ] 
    def customize(self):
        self.is_acolyte = True
        self.fire_count = 0
        self.triggered = False
        self.tick_type = Object.TickTypes.PURGING
        self.snap_type = SnapEnemy.ENEMY
        self.visible = True
        self.z_index = 1
        self.buftarget = "popup"
        self.texture = Acolyte.textures[0]
        self.widx = int(uniform(0.0,40.0))
        self.size = [ 4, 4 ]
        self.physics = { "radius" : 0.35, "mass"   : 0.0005, "friction" : 0.3 }
        #self.state = choice( [ Acolyte.STATE_SEEKING_RANDOM, Skeline.STATE_SEEKING_PLAYER ] )
        self.state = Acolyte.STATE_SEEKING_RANDOM
        self.stimer = 0
        self.rvx = None
        self.speed = 0.8
        self.invert_seek = False
        self.flip_pxy = False

        self.wavidx = 0
        self.snap_effect_emit = 0
        self.iframes = 0
        SnapEnemy.set_combat_vars(self)

        self.hp = 250
        

    def tick(self):
        if(self.floor.player.title_card.displaying()):
            return True
        if(SnapEnemy.handle_tick_disabled(self)):
            return True

        if self.triggered:
            self.floor.add_fog(self, 0.7)
        self.wavidx = self.wavidx + 0.01
        SnapEnemy.tick(self)
        self.widx = (self.widx + 1) % 40
        self.wfr = floor(self.widx/20)
        self.texture = Acolyte.textures[0]
        self.light_type = Object.LightTypes.NONE

        y = self.floor.player.p[0] - self.p[0]
        x = self.floor.player.p[1] - self.p[1]

        md = (x*x)+(y*y)
        if( md < 250 ):
            if not self.triggered:
                self.triggered = True
                if not self.can_see_player():
                    self.triggered = False

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

        calc_speed = self.speed

        if self.state == Acolyte.STATE_SEEKING_PLAYER:
            if(self.stimer == 1):
                KSounds.play(KSounds.acolyte_hustle)
            self.fire_count = 0
            self.rvx = None
            if self.flip_pxy:
                y = self.floor.player.p[0] - self.p[0]
                x = self.floor.player.p[1] - self.p[1]
            else:
                x = self.floor.player.p[0] - self.p[0]
                y = self.floor.player.p[1] - self.p[1]
    


            rad = atan2(y,x)
            vx = cos(rad) * calc_speed
            vy = sin(rad) * calc_speed
            self.v = [ vx,vy]

            if(self.stimer > 25 ):
                self.stimer = 0
                self.state = choice( [ Acolyte.STATE_SEEKING_RANDOM, Skeline.STATE_SEEKING_PLAYER ] )
                self.invert_seek = choice( [ True, False ] )
                if( self.state == Acolyte.STATE_SEEKING_RANDOM ):
                    self.state = choice( [ Acolyte.STATE_SEEKING_RANDOM, Skeline.STATE_CHARGING_SHOT ] )
                    self.flip_pxy = choice( [ True, True, True, False ] )
        if self.state == Acolyte.STATE_SEEKING_RANDOM:
            self.fire_count = 0
            if not self.rvx:
                self.rvx = [ uniform(-1.0,1.0), uniform(-1.0,1.0) ]
                self.flip_pxy = choice( [ True, False ] )
            self.v = [ self.rvx[0] * calc_speed, self.rvx[1] * calc_speed ]
            if(self.stimer > 80 ):
                self.stimer = 0
                self.state = choice( [ Acolyte.STATE_SEEKING_RANDOM, Skeline.STATE_SEEKING_PLAYER, Skeline.STATE_CHARGING_SHOT ] )
                self.invert_seek = choice( [ True, True,True, False ] )
        if self.state == Acolyte.STATE_CHARGING_SHOT:
            if(self.stimer == 10):
                KSounds.play(KSounds.acolyte_hustle)
            self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
            self.light_color = [9.0,0.4,0.1,1.0]
            self.light_radius = uniform(30.0,50.0)
            self.v = [0.0,0.0]
            self.texture = Acolyte.textures[1]
            self.floor.create_object( ChromaticWave( p = [ self.p[0], self.p[1] ] ) )
            if( self.stimer > 25 ):
                self.stimer = 0
                self.state = Acolyte.STATE_FIRING_SHOT
                self.pickTarget()
        if self.state == Acolyte.STATE_FIRING_SHOT:
            if(self.stimer==1):
                KSounds.play_eproj()
            self.texture = Acolyte.textures[2]
            if( self.stimer > 8 ):
                self.fireRanged()
                self.fire_count = self.fire_count + 1
                if self.fire_count >3:
                    self.state = Acolyte.STATE_SEEKING_PLAYER
                    self.fire_count = 0
                else:
                    self.state = Acolyte.STATE_CHARGING_SHOT

        if(self.hp < 0):
            SnapEnemy.die(self)
            return False

        return True

    def pickTarget(self):
        x = self.floor.player.p[0] - self.p[0]
        y = self.floor.player.p[1] - self.p[1]
        rad = atan2(y,x)
        self.target_rad = rad
        
    def fireRanged(self):
        self.flash(1.0,0.8,0.0)
        #x = self.floor.player.p[0] - self.p[0]
        #y = self.floor.player.p[1] - self.p[1]
        #rad = atan2(y,x)
        self.floor.create_object( BasicProjectile( p = [ self.p[0], self.p[1] ], rad = self.target_rad+uniform(-0.1,0.1) ) )
        KSounds.play_eproj()

    def get_shader_params(self):
        bp = SnapEnemy.get_shader_params(self)
        bp['translation_local'][0] = 0.1
        bp['translation_local'][1] = -0.4 + (sin( self.wavidx )*0.2)
        return bp
