from Newfoundland.Object import Object
from .SnapEnemy import SnapEnemy
from random import uniform, choice, randint
from math import sin,cos,atan2,floor,tanh
from Beagle import API as BGL
from client.beagle.Newfoundland.GeometryUtils import segments_intersect
from ..LevelEffects.ChromaticWave import ChromaticWave
from ...KSounds import KSounds
from ..RangedEnemyAttacks.BasicProjectile import BasicProjectile

class Yeller(SnapEnemy):
    def receive_snap_attack(self, was_crit):
        SnapEnemy.receive_snap_attack(self, was_crit)

    def parse(od,df):
        o = Yeller( p = [ od["x"],od["y"] ] )
        SnapEnemy.set_group(o,od)
        df.snap_enemies.append(o)
        df.enemies.append(o)
        df.yellers.append(o)
        return o

    STATE_PACKING = 0
    STATE_HUNTING = 1
    STATE_AMBLING = 2

    textures = BGL.assets.get('KT-forest/animation/screecher')

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
        self.texture = Yeller.textures[0]
        self.widx = 0
        self.size = [ 0.8, 0.8 ]
        self.physics = { "radius" : 0.2, "mass"   : 0.0001, "friction" : 0.0 }
        self.state =  Yeller.STATE_PACKING
        self.stimer = 0
        self.speed = 4.0
        self.circle_dir = 0

        self.snap_effect_emit = 0
        self.iframes = 0
        SnapEnemy.set_combat_vars(self)
        self.hp = 50
        
    def custom_die(self):
        self.floor.yellers.remove(self)

    def tick(self):

        if(self.floor.player.title_card.displaying()):
            return True
        if(SnapEnemy.handle_tick_disabled(self)):
            return True
        if self.triggered:
            self.floor.add_fog(self, 0.30)

        SnapEnemy.tick(self)
        self.widx = (self.widx + 1) % (len(Yeller.textures)*4)
        self.wfr = self.widx//4
        self.texture = Yeller.textures[self.wfr]
        self.light_type = Object.LightTypes.NONE

        y = self.floor.player.p[0] - self.p[0]
        x = self.floor.player.p[1] - self.p[1]
        md = (x*x)+(y*y)
        if md < 900:
            if not self.triggered:
                self.triggered = True
        if md > 900:
            self.triggered = False

        if not self.triggered:
            if self.hp < 0:
                SnapEnemy.die(self)
                return False
            return True

        self.visible = True

        if self.state == Yeller.STATE_PACKING:
            # find a pack and move towards it and slighty away from the player
            closest = self.packYeller()

            vx = cos(self.target_rad) * self.speed
            vy = sin(self.target_rad) * self.speed

            self.v[0] = vx
            self.v[1] = vy
            if self.stimer > 15:
                self.state = choice([Yeller.STATE_HUNTING, Yeller.STATE_PACKING])
                self.stimer = 0

        if self.state == Yeller.STATE_HUNTING:
            # in a pack hunting the player
            player = self.pickTarget()

            vx = cos(self.target_rad) * self.speed
            vy = sin(self.target_rad) * self.speed

            self.v[0] = vx
            self.v[1] = vy
            if self.stimer > 40:
                self.state = choice([Yeller.STATE_HUNTING, Yeller.STATE_PACKING])
                self.stimer = 0

        if self.state == Yeller.STATE_AMBLING:
            # in a pack but too far away to hunt 
            pass

        self.stimer += 1
        
        if(self.hp < 0):
            SnapEnemy.die(self)
            return False

        return True

    def attempt_melee(self):
        # if the state is hunting then it should check for melee attack to me in range
        # only the charging state is one that will be them attempting attack
        pass

    def pickTarget(self):
        x = (self.floor.player.p[0] - self.p[0])+self.floor.player.v[0]
        y = (self.floor.player.p[1] - self.p[1])+self.floor.player.v[1]
        rad = atan2(y,x)
        self.target_rad = rad
        return rad

    def packYeller(self):
        if len(self.floor.yellers) == 0:
            return 0.0
        
        ax = self.p[0]
        ay = self.p[1]
        i = 1
        for yell in self.floor.yellers:
            yx = abs(yell.p[0] - self.p[0])
            yy = abs(yell.p[1] - self.p[1])
            ymd = (yx*yx)+(yy*yy)
            if ymd < 40:
                ax += yell.p[0]
                ay += yell.p[1]
                i += 1
        if i == 1:
            return self.closestYeller()

        ax /= i
        ay /= i
        x = (ax - self.p[0])
        y = (ay - self.p[1])
        rad = atan2(y,x)
        self.target_rad = rad
        return rad

    def closestYeller(self):
        if len(self.floor.yellers) == 0:
            return 0.0
        ax = abs(self.floor.yellers[0].p[0] - self.p[0])
        ay = abs(self.floor.yellers[0].p[1] - self.p[1])
        cp = self.floor.yellers[0].p
    
        for yell in self.floor.yellers:
            if ax > abs(yell.p[0] - self.p[0]) and ay > abs(yell.p[1] - self.p[1]):
                ax = abs(yell.p[0] - self.p[0])
                ay = abs(yell.p[1] - self.p[1])
                cp = yell.p
        
        x = (cp[0] - self.p[0])
        y = (cp[1] - self.p[1])
        rad = atan2(y,x)
        self.target_rad = rad
        return rad

    def next_state( self, state ):
        self.stimer = 0
        self.state = state
    
    def get_shader_params(self):

        # this is how you adjust centering of a sprite to match the physics when the bitmap doesn't line up...

        bp = SnapEnemy.get_shader_params(self)
        bp['translation_local'][0] = 0.0
        bp['translation_local'][1] = -0.7
        return bp
