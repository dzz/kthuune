from Newfoundland.Object import Object
from .SnapEnemy import SnapEnemy
from random import uniform, choice
from math import sin,cos,atan2,floor,hypot
from Beagle import API as BGL
from client.beagle.Newfoundland.GeometryUtils import segments_intersect
from ..LevelEffects.ChromaticWave import ChromaticWave
from ...KSounds import KSounds
from ..Configuration.vconf import vconf
from ...KPlayer import Sword

class Worm(SnapEnemy):
   
    textures = [
        BGL.assets.get("KT-forest/texture/worm0000"),
        BGL.assets.get("KT-forest/texture/worm0001"),
        BGL.assets.get("KT-forest/texture/worm0002"),
        BGL.assets.get("KT-forest/texture/worm0003"),
    ] 

    def get_firefly_count(self):
        return 1

    def get_kill_particles(self):
        return 2

    def customize(self):
        self.triggered = False
        self.hp = 5 + choice(range(0,30))
        self.dead = False
        self.tick_type = Object.TickTypes.PURGING
        self.fridx = choice(range(0,480))
        self.worm_target = None
        self.physics = { "radius" : 0.5, "mass"   : 0.0003, "friction" : 0.0 }
        self.fworm_target = [0.0,0.0]
        self.next_choice = 90
        self.buftarget = "popup"
        self.size = [1.2,1.2]
        self.attacking = False
        self.z_index = 1
        self.biting = False
        self.snap_type = SnapEnemy.ENEMY
        self.iframes = 0
        self.defense = 3
        self.lifetime = 0
        
    def pick_target(self):
        rad = None
        speed = None
        if self.dist2( self.floor.player) < 100:
            x = self.floor.player.p[0] - self.p[0]
            y = self.floor.player.p[1] - self.p[1]
            rad = atan2(-1*y,x)
            speed = uniform(4.0,10.0)
            self.attacking = True
        else:
            rad = uniform(-3.14,3.14)
            speed = uniform(0.2,1.3)
            self.attacking = False

        if(uniform(0.0,1.0)>0.06):
            self.worm_target = [ cos(rad)*speed, -1*sin(rad)*speed ]
        else:
            self.worm_target = [ cos(-1*rad)*speed, -1*sin(-1*rad)*speed ]

        self.next_choice = 2

    def should_draw(self):
        p = self.get_shader_params()['translation_world']
        visRad = vconf.visRad
        if(p[0]<-visRad): return False
        if(p[1]<-visRad): return False
        if(p[0]>visRad): return False
        if(p[1]>visRad): return False
        return True

    def tick(self):

        self.lifetime+=1
        if(self.lifetime>10):
            self.triggered = True
        if(self.floor.player.kill_success):
            return True

        if(self.dead):
            self.color = [0.0,0.0,0.0,1.0]
            self.buftarget="floor"
            return True

        if(uniform(0.0,1.0)>0.6):
            return True

        if not self.should_draw():
            return True

        self.rad = atan2( self.fworm_target[1], self.fworm_target[0] )
        self.fridx = self.fridx + 1

        if self.attacking:
            tidx = int(self.fridx/15)%4
        else:
            tidx = int(self.fridx/24)%4

        self.texture = Worm.textures[tidx]

        if(not self.worm_target):
            self.pick_target()
        elif (self.fridx%self.next_choice) == 0:
            self.pick_target()

        freq = 20
        self.biting = False
        if self.attacking:
            freq = 5
        if(self.fridx%freq)==0:
            self.fworm_target[0] = (self.fworm_target[0]*0.8) + (self.worm_target[0]*0.2)
            self.fworm_target[1] = (self.fworm_target[1]*0.8) + (self.worm_target[1]*0.2)

            if self.attacking: 
                if tidx == 3: 
                    self.biting = True

        rsize = self.size
        if(tidx>2):
            rsize = [1.6,1.6]
        elif(tidx==0):
            rsize = [1.4,1.4]
        elif(tidx==1):
            rsize = [1.1,1.1]

        self.size[0] = (self.size[0] *0.7) + (rsize[0]*0.3)
        self.size[1] = (self.size[1] *0.7) + (rsize[1]*0.3)
        self.v[0] = self.fworm_target[0] * (float((tidx)+0.1)*0.25)
        self.v[1] = self.fworm_target[1] * (float((tidx)+0.1)*0.25)


        self.color = [1.0,1.0,1.0,1.0]
        self.light_type = Object.LightTypes.NONE
        if self.attacking:
            self.color = [uniform(0.5,1.0),uniform(0.0,1.0),0.0,1.0]
        if self.biting:
            self.v[0] = self.v[0]*4
            self.v[1] = self.v[1]*4
            self.color = [0.0,1.0,0.0,1.0]
            self.light_color = [uniform(0.0,1.0),uniform(0.0,1.0),0.0,1.0]
            self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
            self.light_radius = uniform(10.0,20.0)

            if hypot(self.floor.player.p[0] - self.p[0], self.floor.player.p[1] - self.p[1] ) < 2.0:
                self.floor.player.enemy_attack(3)
                self.attack_str = 2
                self.vx = self.v[0] * 0.4
                self.vy = self.v[1] * 0.4
                self.floor.player.receive_ranged_attack(self)

        if (not self.biting):
            if hypot(self.floor.player.p[0] - self.p[0], self.floor.player.p[1] - self.p[1] ) < 7.0:
                if(self.floor.player.sword.state == Sword.STATE_DISCHARGING) or (self.floor.player.sword.state == Sword.STATE_SPIN_ATTACK):
                    self.hp -= 1.5
                    self.floor.player.notify_succesful_attack()
                    self.floor.player.next_dashcombo()
                    self.v[0] = self.v[0]*-8
                    self.v[1] = self.v[1]*-8
                    self.floor.create_object( SpikeyWave( p = self.p ) )

        if(self.hp<0.0):
            SnapEnemy.die(self)
            for fi in range(0,3):
                self.floor.create_object( ChromaticWave( p = [ self.p[0], self.p[1] ] ) )
            return False

        return True
