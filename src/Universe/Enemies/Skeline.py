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
        SnapEnemy.set_group(o,od)
        df.snap_enemies.append(o)
        df.enemies.append(o)
        return o

    STATE_SEEKING_RANDOM = 0
    STATE_SEEKING_PLAYER = 1
    STATE_CHARGING_SHOT = 2
    STATE_FIRING_SHOT = 3

    textures = BGL.assets.get("KT-forest/animation/skeline")

    def customize(self):

        self.op = list(self.p)
        self.triggered = False
        self.tick_type = Object.TickTypes.PURGING
        self.snap_type = SnapEnemy.ENEMY
        self.visible = True
        self.z_index = 1
        self.buftarget = "popup"
        self.texture = Skeline.textures[0]
        self.widx = int(uniform(0.0,40.0))
        self.size = [ 2.8, 2.8 ]
        self.physics = { "radius" : 1.3, "mass"   : 0.0005, "friction" : 0.0 }
        self.state = choice( [ Skeline.STATE_SEEKING_RANDOM, Skeline.STATE_SEEKING_PLAYER ] )
        #self.state = Skeline.STATE_SEEKING_RANDOM
        self.stimer = 0

        self.snap_effect_emit = 0
        self.iframes = 0
        SnapEnemy.set_combat_vars(self)
        self.hp = 50
        self.tooltip_time = choice([10,20,50,150,300])
        self.next_tooltip = 250

        self.rvx = None
        self.speed = 3.8
        self.run_away = False

    def tick(self):
        if(self.triggered):
            self.tooltip_time = self.tooltip_time +1
        else:
            self.tooltip = None

        if self.tooltip_time > 200:
            self.tooltip = None
        if self.tooltip_time > self.next_tooltip:
            self.next_tooltip = choice([250,200,333])
            self.tooltip = choice([
                #"come get me!",
                "you suck!",
                #"i hate your face!",
                #"i hate your sword!",
                #"i am going to kill you!",
                "hey, get blasted!",
                "suck my eggs!",
                #"hasta lavsita... baby",
                "!@#$!",
                "eat my shorts",
                #"sinner!",
                #"blasphemer!"
                #"hey, you can call me rip",
                #"hey you can call me YOU'RE DEAD"
                ])
            self.tooltip_time = 0


        if(self.floor.player.title_card.displaying()):
            return True
        if(SnapEnemy.handle_tick_disabled(self)):
            return True
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
        if( md > 300 ):
            self.triggered = False

        if not self.triggered:
            if(self.hp < 0):
                SnapEnemy.die(self)
                return False
            #self.visible = False
            return True

        self.visible = True

        self.stimer += 1

        if self.state == Skeline.STATE_SEEKING_PLAYER:

            #seek player unless acolyte is closer
            p = self.floor.player.p
            pscore = abs(p[0] - self.p[0]) + abs(p[1]-self.p[1])
            for enemy in self.floor.snap_enemies:
                if not self.run_away and "is_acolyte" in enemy.__dict__ and enemy.triggered:
                    ascore = abs(enemy.p[0] - self.p[0]) + abs(enemy.p[1]-self.p[1]) * 0.8
                    if ascore<pscore:
                        self.run_away = False
                        p=enemy.p
                        break

            x = p[0] - self.p[0]
            y = p[1] - self.p[1]

            rad = atan2(y,x)
            vx = cos(rad) * self.speed
            vy = sin(rad) * self.speed
            if self.run_away:
                self.v = [vx*-1, vy*-1]
            else:
                self.v = [vx, vy]


            if self.stimer > 25:
                self.stimer = 0
                self.state = choice( [Skeline.STATE_CHARGING_SHOT, Skeline.STATE_SEEKING_RANDOM, Skeline.STATE_SEEKING_PLAYER, Skeline.STATE_SEEKING_PLAYER ] )
                if self.state == Skeline.STATE_SEEKING_PLAYER:
                    #if its still seeking the player have a chance of running away
                    self.run_away = choice( [ False, True, False ] )
        if self.state == Skeline.STATE_SEEKING_RANDOM:
            if not self.rvx:
                self.rvx = [ uniform(-1.0,1.0), uniform(-1.0,1.0) ]
            self.v = [ self.rvx[0] * self.speed, self.rvx[1] * self.speed ]
            if self.stimer > 10:
                self.stimer = 0
                self.state = choice( [ Skeline.STATE_SEEKING_RANDOM, Skeline.STATE_SEEKING_PLAYER, Skeline.STATE_SEEKING_PLAYER ] )
                if self.state == Skeline.STATE_SEEKING_PLAYER:
                    #if its still seeking the player have a chance of running away
                    self.run_away = choice( [ False, True, False ] )

        if self.state == Skeline.STATE_CHARGING_SHOT:
            if self.stimer == 1:
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
            self.floor.player.pump_timer('skeline')
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
        self.floor.create_object( BasicProjectile( p = [ self.p[0], self.p[1] ], rad = self.target_rad, animation = 2 ) )
        KSounds.play_eproj()

    def get_shader_params(self):
        bp = SnapEnemy.get_shader_params(self)
        bp['translation_local'][0] = 0.0
        bp['translation_local'][1] = -0.7
        return bp

