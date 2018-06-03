from Newfoundland.Object import Object
from .SnapEnemy import SnapEnemy
from random import uniform, choice, randint
from math import sin,cos,atan2,floor,tanh
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

    STATE_WAITING = 0
    STATE_CIRCLING = 1
    STATE_CHARGING = 2
    STATE_CLIMBING = 3

    textures = BGL.assets.get('KT-forest/animation/spider')[4:]

    #this is the best function ever, its like init...
    # but it happens later.
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
        self.state =  Spider.STATE_WAITING
        self.stimer = 0
        self.speed = 4.0
        self.circle_dir = 0
        self.distance_mod = 1

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
        if md < 300:
            if not self.triggered:
                self.triggered = True
        if md > 300:
            self.triggered = False

        if not self.triggered:
            if self.hp < 0:
                SnapEnemy.die(self)
                return False
            return True

        self.visible = True

        #get the distance as a factor between 0:1
        self.distance_mod = 1-tanh(md/300)

        if self.state == Spider.STATE_WAITING:
            #this is to halt rapidly increasing the unpredictability of their movement
            if self.v[0] > 0.01:
                self.v[0] /= 2
            if self.v[1] > 0.01:
                self.v[1] /= 2

            if self.stimer > 60:
                self.state = choice([Spider.STATE_WAITING, Spider.STATE_CIRCLING, Spider.STATE_CIRCLING, Spider.STATE_CHARGING])
                self.stimer = 0
        if self.state == Spider.STATE_CIRCLING:
            self.pickTarget()
            if self.stimer % 10 == 0:
                old_dir = self.circle_dir
                self.circle_dir = choice([1.57-(self.distance_mod-1), 4.71+(self.distance_mod-1)])
                if self.circle_dir != old_dir:
                    self.size[0] *= -1
            
            rad = self.target_rad + self.circle_dir
            
            vx = cos(rad) * 1.8 * self.speed
            vy = sin(rad) * 1.8 * self.speed

            self.v[0] = vx
            self.v[1] = vy

            if self.stimer > 30:
                self.state = choice([Spider.STATE_CIRCLING,Spider.STATE_CHARGING])
                self.stimer = 0

        if self.state == Spider.STATE_CHARGING:
            self.pickTarget()

            if md <= 50:
                speed_mod = 3 * self.distance_mod
                self.attempt_melee()
            else:
                speed_mod = 1

            vx = cos(self.target_rad) * (self.speed * speed_mod)
            vy = sin(self.target_rad) * (self.speed * speed_mod)

            self.v[0] = vx
            self.v[1] = vy

            if self.stimer > 20:
                self.state = choice([Spider.STATE_WAITING,Spider.STATE_CHARGING,Spider.STATE_CIRCLING])
                self.stimer = 0



        self.stimer += 1
        
        if(self.hp < 0):
            SnapEnemy.die(self)
            return False

        return True

    def attempt_melee(self):
        # if the state is charging then it should check for melee attack to me in range
        # only the charging state is one that will be them attempting attack
        pass

    def pickTarget(self):
        x = (self.floor.player.p[0] - self.p[0])+self.floor.player.v[0]
        y = (self.floor.player.p[1] - self.p[1])+self.floor.player.v[1]
        rad = atan2(y,x)
        self.target_rad = rad

    def next_state( self, state ):
        self.stimer = 0
        self.state = state
    
    def get_shader_params(self):

        # this is how you adjust centering of a sprite to match the physics when the bitmap doesn't line up...

        bp = SnapEnemy.get_shader_params(self)
        bp['translation_local'][0] = 0.0
        bp['translation_local'][1] = -0.7
        return bp
