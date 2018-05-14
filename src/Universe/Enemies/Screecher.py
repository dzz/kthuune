from Newfoundland.Object import Object
from .SnapEnemy import SnapEnemy
from random import uniform, choice
from math import sin,cos,atan2,floor
from Beagle import API as BGL
from client.beagle.Newfoundland.GeometryUtils import segments_intersect
from ..LevelEffects.ChromaticWave import ChromaticWave
from ...KSounds import KSounds
from ..RangedEnemyAttacks.BasicProjectile import BasicProjectile

class Screecher(SnapEnemy):
    def receive_snap_attack(self, was_crit):
        SnapEnemy.receive_snap_attack(self, was_crit)

    def parse(od,df):
        o = Screecher( p = [ od["x"],od["y"] ] )
        SnapEnemy.set_group(o,od)
        df.snap_enemies.append(o)
        df.enemies.append(o)
        return o

    STATE_SQUATTING = 0
    STATE_DIVING = 1
    STATE_BIRTHING = 3

    textures = BGL.assets.get('KT-forest/animation/screecher')
    def customize(self):

        self.op = list(self.p)
        self.triggered = False
        self.tick_type = Object.TickTypes.PURGING
        self.snap_type = SnapEnemy.ENEMY
        self.visible = True
        self.z_index = 1
        self.buftarget = "popup"
        self.texture = Screecher.textures[0]
        self.widx = int(uniform(0.0,40.0))
        self.base_size = [ 1.7, 1.56 ]
        self.size = list(self.base_size)
        self.physics = { "radius" : 0.38, "mass"   : 0.0009, "friction" : 0.0 }
        self.state =  Screecher.STATE_BIRTHING 
        self.stimer = 0
        self.rvx = None
        self.speed = 3.8
        self.invert_seek = False
        self.flip_pxy = False
        self._t = uniform(0.0,100.0)

        self.snap_effect_emit = 0
        self.iframes = 0
        SnapEnemy.set_combat_vars(self)
        self.hp = 50
        self.tooltip_time = choice([10,20,50,150,300])
        self.next_tooltip = 250

        self.dive_state_trigger = choice ( [ 180,190,203,208,217] )
        self.cyclonic_direction = uniform(0.1,0.3)

        self.birth_burst = [ uniform(-1.0,1.0), uniform(0.5,1.2) ]
        self.birth_amt = 0.0
        self.birth_scale = 1.0 + uniform(0.01,0.04)
        

    def tick(self):

        self._t += 0.01

        self.size[0] = self.base_size[0] + ((sin(self._t)*0.35) + (self.rad*0.1)*0.85)
        self.size[1] = self.base_size[1] + ((abs(cos(self._t))*0.35) - (self.rad*0.1)*0.8)
        self.rad = sin(self._t*cos(self._t)) *0.1

        if(self.floor.player.title_card.displaying()):
            return True
        if(SnapEnemy.handle_tick_disabled(self)):
            return True
        if self.triggered:
            self.floor.add_fog(self, 0.30)

        SnapEnemy.tick(self)
        self.widx = (self.widx + 1) % 40
        self.wfr = floor(self.widx/5)
        self.texture = Screecher.textures[self.wfr]
        self.light_type = Object.LightTypes.NONE

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
        self.stimer = self.stimer + 1

        self.stimer += 1
        #######
        if self.state == Screecher.STATE_BIRTHING:
            self.flash_color = [ 1.0,1.0,0.0,1.0 ]
            self.rad = uniform(-0.3,0.3)
            self.v[0] = self.birth_burst[0]*0.2
            self.v[1] = self.birth_burst[1]*0.2
            self.birth_burst[1]*=0.9
            self.size[0] = self.birth_amt*self.base_size[0]
            self.size[1] = self.birth_amt*self.base_size[1]
            self.birth_amt += 0.01
            self.birth_amt *= self.birth_scale
            if(self.birth_amt>1.0):
                self.floor.sounds.play(choice([ self.floor.sounds.ree1, self.floor.sounds.ree2 ]) )
                self.next_state( Screecher.STATE_DIVING )

        if self.state == Screecher.STATE_SQUATTING:
            if(self.stimer > self.dive_state_trigger):
                self.floor.sounds.play(choice([ self.floor.sounds.ree1, self.floor.sounds.ree2 ]) )
                self.next_state( Screecher.STATE_DIVING )
        if self.state == Screecher.STATE_DIVING:
            self._t += 0.01 # increase shudder
            dx,dy = self.floor.player.p[0] - self.p[0], self.floor.player.p[1] - self.p[1],
            l = abs(dx)+abs(dy) 
            if(l<0.1):
                l = 0.1
            dx,dy = dx/l,dy/l
    
            rad = atan2(dx,dy)
            rad += (self.cyclonic_direction)*( (150.0-l)*0.04)

            dx,dy = sin(rad),cos(rad)

            self.v[0] = dx*10.0
            self.v[1] = dy*10.0

            if(self.stimer > 100):
                self.cyclonic_direction *= -1
                self.next_state( Screecher.STATE_SQUATTING )
            
        if(self.hp < 0):
            SnapEnemy.die(self)
            return False

        return True

    def next_state( self, state ):
        self.stimer = 0
        self.state = state
    
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
