from Newfoundland.Object import Object
from .SnapEnemy import SnapEnemy
from random import uniform, choice
from math import sin,cos,atan2,floor,pi
from Beagle import API as BGL
from client.beagle.Newfoundland.GeometryUtils import segments_intersect
from ..LevelEffects.ChromaticWave import ChromaticWave
from ...KSounds import KSounds
from ..RangedEnemyAttacks.BasicProjectile import BasicProjectile
from ..Hazards.WormField import WormField

class Stork(SnapEnemy):

    def custom_die(self):
        wf_spec = [ self.p[0], self.p[1], 15 ]
        self.floor.create_object( WormField( wf_spec = wf_spec) )

    def get_shader_params(self):
        bp = SnapEnemy.get_shader_params(self)
        bp['translation_local'][0] = 0.1
        bp['translation_local'][1] = -0.4
        return bp

    def receive_snap_attack(self, was_crit):
        SnapEnemy.receive_snap_attack(self, was_crit)

    def parse(od,df):
        o = Stork( p = [ od["x"],od["y"] ] )
        SnapEnemy.set_group(o,od)
        df.snap_enemies.append(o)
        return o

    STATE_WAITING = 0
    STATE_LEAPING = 1
    STATE_LANDING = 2

    textures = [
        BGL.assets.get("KT-forest/texture/stork0000"),
        BGL.assets.get("KT-forest/texture/stork0001"),
        BGL.assets.get("KT-forest/texture/stork0002")
    ] 
    def customize(self):
        self.fire_count = 0
        self.triggered = False
        self.tick_type = Object.TickTypes.PURGING
        self.snap_type = SnapEnemy.ENEMY
        self.visible = True
        self.z_index = 1
        self.buftarget = "popup"
        self.texture = Stork.textures[0]
        self.widx = int(uniform(0.0,40.0))
        self.size = [ 4, 4 ]
        self.physics = { "radius" : 0.35, "mass"   : 0.0005, "friction" : 0.0 }
        #self.state = choice( [ Stork.STATE_SEEKING_RANDOM, Skeline.STATE_SEEKING_PLAYER ] )
        self.state = Stork.STATE_WAITING
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
        if self.triggered:
            self.floor.add_fog(self, 0.5)

        y = self.floor.player.p[0] - self.p[0]
        x = self.floor.player.p[1] - self.p[1]

        md = (x*x)+(y*y)
        if( md < 250 ):
            if not self.triggered:
                self.triggered = True
                if not self.can_see_player():
                    self.triggered = False

        if not self.triggered:
            if(self.hp < 0):
                SnapEnemy.die(self)
                return False
            return True

        self.stimer = self.stimer + 1

        fridx = int( (self.stimer % 80) / 40)
        self.texture = Stork.textures[fridx]

        SnapEnemy.tick(self)

        if(self.state == Stork.STATE_WAITING):
            if(self.stimer==100):
                KSounds.play(KSounds.lifting_off)

            if self.stimer > 120:
                self.target_p = list(self.floor.player.p)
                self.stimer = 0
                self.state = Stork.STATE_LEAPING
                self.physics_suspended = True
                self.floor.snap_enemies.remove(self)

        if(self.state == Stork.STATE_LEAPING):
            self.fire_idx = 0
            self.texture = Stork.textures[2]
            self.p[1] = self.p[1] - 0.5
            self.size[0] = self.size[0] + 0.5
            self.size[1] = self.size[1] + 0.5
            if(self.stimer > 60):
                self.stimer = 0
                self.state = Stork.STATE_LANDING

        if(self.state == Stork.STATE_LANDING):
            self.size = [ 4, 4 ]
            self.texture = Stork.textures[2]
            dx = self.target_p[0] - self.p[0]
            dy = self.target_p[1] - self.p[1]

            self.p[0] = self.p[0] + (dx*0.2)
            self.p[1] = self.p[1] + (dy*0.2)


            if(self.stimer>40):
                self.p[0] = self.target_p[0]
                self.p[1] = self.target_p[1]
                self.physics_suspended = False
                if not self in self.floor.snap_enemies:
                    self.floor.snap_enemies.append(self)
                if(self.stimer % 15 == 0):
                    self.fire_circle()
                    self.fire_idx = self.fire_idx + 1
                if(self.stimer>(40+(15*3))):
                    self.stimer = 0
                    self.state = Stork.STATE_WAITING

        if(self.hp < 0):
            SnapEnemy.die(self)
            return False
        return True

    def fire_circle(self):
        num_shots = 3
        rad = (pi*2)/num_shots
        KSounds.play_eproj()
        #for x in range(0,num_shots):
        #    self.floor.create_object( BasicProjectile( p = [ self.p[0], self.p[1] ], rad = rad * x ) )
        x = self.fire_idx
        self.floor.create_object( BasicProjectile( p = [ self.p[0], self.p[1] ], rad = rad * x ) )
