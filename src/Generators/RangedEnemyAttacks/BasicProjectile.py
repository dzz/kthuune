from Newfoundland.Object import Object
from random import uniform, choice
from math import sin,cos,atan2,floor
from Beagle import API as BGL
from client.beagle.Newfoundland.GeometryUtils import segments_intersect
from ..LevelEffects.SpikeyWave import SpikeyWave
from ..Particles.SplatterParticle import SplatterParticle
from ...KSounds import KSounds

class BasicProjectile(Object):
    texture = BGL.assets.get("KT-player/texture/flare")
    def __init__(self,**kwargs):
        Object.__init__(self,**kwargs)
        self.texture = BasicProjectile.texture
        self.buftarget = "popup"
        self.tick_type = Object.TickTypes.PURGING
        self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
        self.light_radius = 5
        self.lifespan = 120
        self.light_color = [ 0.6,1.0,0.3,0.4 ]

        self.size = [ 0.5,0.5 ]
        self.snapshot_fields = [ 'p' ]

        spd = 0.45 + uniform(0.001, 0.01)
        self.vx = cos( self.rad )*spd
        self.vy = sin( self.rad )*spd
        
        self.attack_str = 8
        self.player_touch_frames = 0

        self.vs_enemy = False
        
    def reorient(self):
        self.vs_enemy = True
        KSounds.play( KSounds.redirect )
        self.lifespan = 80
        spd = (0.55 + uniform(0.001, 0.01))*1.7
        self.vx = cos( self.rad )*spd
        self.vy = sin( self.rad )*spd

    def tick(self):


        deadly = False
        if(self.size[0] < 1.5):
            growth = 1.2
            self.size[0] *= growth
            self.size[1] *= growth
        else:
            deadly = True
        self.light_color[1] = uniform(0.4,0.8)
        self.light_color[0] = uniform(0.0,1.0)
        self.light_color[3] = uniform(0.0,1.0)
        self.light_radius = uniform(15,40)
        self.p[0] = self.p[0] + self.vx 
        self.p[1] = self.p[1] + self.vy 
        self.lifespan = self.lifespan - 1

        segment = [
                    [self.snapshot['p'][0], self.snapshot['p'][1]],
                    [self.p[0], self.p[1] ]
                  ]

        for blocker in self.floor.get_light_occluders():
            if segments_intersect( segment, blocker):
                self.lifespan = 0
                break                

        if not deadly:
            return True

        if self.vs_enemy:
            for enemy in self.floor.snap_enemies:
                if(enemy.snap_type == 1):
                    dx = self.p[0] - enemy.p[0]
                    dy = self.p[1] - enemy.p[1]
                    dx = dx * dx
                    dy = dy * dy
                    md = dx+dy
                    if md < 5:
                        enemy.receive_snap_attack(False)
                        self.floor.objects.remove(self)
                        return False
        else:
            dx = self.p[0] - self.floor.player.p[0]
            dy = self.p[1] - self.floor.player.p[1]
    
            dx = dx * dx
            dy = dy * dy

            md = dx+dy

            if md < 6.5:
                self.player_touch_frames += 1

                if(self.player_touch_frames>7):
                    self.floor.player.receive_ranged_attack(self)
                    self.floor.create_object( SpikeyWave( p = self.p, color=[1.0,0.0,0.0,1.0] ) )
                    self.floor.objects.remove(self)

                    for x in range(0,25):
                        self.floor.create_object(SplatterParticle( p = [self.floor.player.p[0], self.floor.player.p[1]], rad = uniform(-3.14,3.14)))
                    return False
                else:
                    if self.floor.player.slash.visible:
                        self.rad = self.floor.player.slash.rad
                        self.reorient()
                        self.player_touch_frames = 0
                    return True

        if(self.lifespan>0):
            return True
        self.floor.objects.remove(self)
        return False
