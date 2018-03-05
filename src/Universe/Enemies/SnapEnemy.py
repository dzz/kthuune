from Newfoundland.Object import Object
from client.beagle.Newfoundland.GeometryUtils import segments_intersect

from ..Particles.Firefly import Firefly
from ..Particles.SplatterParticle import SplatterParticle
from ..LevelEffects.SwordCrit import SwordCrit
from ..LevelEffects.AttackInfo import AttackInfo
from ..LevelEffects.Blood import Blood
from ..LevelEffects.SpikeyWave import SpikeyWave
from ..LevelEffects.Explosion import Explosion
from ..LevelEffects.SkullDeath import SkullDeath
from ..Pickups.HealthVial import HealthVial

from .Spawner import Spawner

from random import uniform
from math import floor
from Beagle import API as BGL

class SnapEnemy(Object):
    TOTEM = 0
    ENEMY = 1

    def handle_tick_disabled(self):
        if not self.group_active:
            self.visible = False
            return True
        return False

    def get_firefly_count(self):
        return 5

    def custom_die(self):
        pass

    def is_cleric(self):
        return False

    def set_group(o,od):
        o.group = 0
        if "group" in od["meta"]:
            o.group = od["meta"]["group"]

        if o.group==0:
            o.group_active = True
        else:
            o.group_active = False
            o.physics_suspended = True
            o.p[0] -= 99999 #sweet hax, don't want the physics running until
                            #active, but don't want to rewrite the binding code,
                            # so just move it faaaar away until its needed
            o.p[1] -= 99999

    def can_see_player(self):
        test_segment = [ [ self.floor.player.p[0], self.floor.player.p[1] ], [self.p[0], self.p[1] ] ]
        for segment in self.floor.get_light_occluders():
            if segments_intersect( segment, test_segment ):
                return False
        return True

    def die(self):

        self.floor.player.boost_run_stamina()
        #self.floor.player.add_dm_message("You killed an enemy")
        if self in self.floor.objects:
            #hack
            self.floor.objects.remove(self)
        if(self in self.floor.snap_enemies):
            self.floor.snap_enemies.remove(self)
        self.floor.create_object( SkullDeath( p = [ self.p[0], self.p[1] ] ) )
        self.floor.player.set_hud_message("KILL!", 60)
        self.floor.player.add_sequence_kill()
        self.floor.player.notify_enemy_killed()
        self.floor.freeze_frames = 3
        
        if(uniform(0.0,1.0) > 0.85):
            self.floor.create_object(HealthVial(p=[ self.p[0], self.p[1]]))

        self.floor.create_object(Blood(p=[self.p[0],self.p[1]]))
        self.custom_die()

        if not self.floor.playing_genocide():
            if not self.skips_spawn():
                self.floor.create_object( Spawner( p = list(self.p), loser = self ) )
        for x in range(0,self.get_kill_particles()):
            spltr = SplatterParticle( p = [self.floor.player.p[0], self.floor.player.p[1]], rad = uniform(-3.14,3.14))
            spltr.color = [0.0,0.0,0.0,1.0]
            spltr.light_color = [ 0.0,1.0,0.0,1.0]
            spltr.size[0]*=uniform(1.0,1.5)
            self.floor.create_object(spltr)

        for x in range(0, self.get_firefly_count()):
            self.floor.create_object( Firefly( p = [ self.p[0], self.p[1] ] ))
        self.floor.player.impulse_hittables()
        self.floor.create_object( Explosion( p = [ self.p[0], self.p[1] ] ))


    def skips_genocide(self):
        return False

    def skips_spawn(self):
        return False
    def get_kill_particles(self):
        return 15

    def parse(od,df):
        o = SnapEnemy( p = [ od["x"],od["y"] ] )
        df.snap_enemies.append(o)
        return o

    def raise_critical_attack(self):
        self.snap_effect_emit = 20
        self.floor.player.notify_crit()
        self.floor.create_object( SwordCrit( p = [ self.p[0], self.p[1]-30 ]))

    def flash(self,r,g,b):
        self.flash_color = [ r,g,b,1.0 ]

    def receive_snap_attack(self, was_crit):

        self.iframes = 20
        self.snap_effect_emit = 10

        crit = 1

        #if(uniform(0.0,1.0)< (self.floor.player.crit_chance*self.floor.player.get_crit_mod())):
        if was_crit:
            crit = 1.8
            print("CRITICAL")
            self.raise_critical_attack()

        attack_amt = (self.floor.player.attack_str*crit) - self.defense

        if(attack_amt<=0):
            attack_amt = 1

        attack_amt += uniform(0, self.floor.player.attack_bonus) * self.floor.player.attack_str

        attack_amt = floor(attack_amt)
        print("ATTACK -> {0}".format(attack_amt))

        self.flash(1.0,0.0,0.0)
        self.floor.create_object(AttackInfo( p=[ self.p[0], self.p[1] ], message="{0}".format(attack_amt)))
        self.hp = self.hp - attack_amt

        for x in range(0,5):
            spltr = SplatterParticle( p = [self.floor.player.p[0], self.floor.player.p[1]], rad = uniform(-3.14,3.14))
            spltr.color = [0.0,0.0,0.0,1.0]
            spltr.light_color = [ 0.0,1.0,0.0,1.0]
            spltr.size[0]*=uniform(1.0,1.5)
            self.floor.create_object(spltr)

        if self.floor.player.snap_animation_buffer>0 and self.hp<=0:
            r = self.tick()
            if not r:
                if self in self.floor.purging_tick_manager.tickables:
                    self.floor.purging_tick_manager.tickables.remove(self)

    def fade_flash(self):
        if(self.flash_color[3]>0.1):
            self.flash_color[3] *= 0.935
        else:
            self.flash_color[3] = 0.0

    def tick(self):
        self.fade_flash()

        if(self.iframes>0):
            self.iframes -=1
        if(self.snap_effect_emit>0):
            self.snap_effect_emit = self.snap_effect_emit - 1
            self.floor.create_object( SpikeyWave( p = self.p ) )

        self.light_radius = uniform(2.0,12.0)
        return True

    def customize(self):
        self.flash_color = [ 1.0,0.0,0.0,1.0 ]
        self.snap_type = SnapEnemy.ENEMY
        self.snap_effect_emit = 0
        self.tick_type = Object.TickTypes.PURGING
        self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
        self.light_radius = 10.0
        self.light_color = [ 1.0, 0.8, 0.0, 1.0 ]
        self.visible = True
        self.z_index = 1
        self.buftarget = "popup"
        self.texture = Skeline.textures[2]
        self.size = [ 1.75, 1.75 ]
        self.set_combat_vars(self)

    def set_combat_vars(self):
        self.hp = 85
        self.defense = 10
