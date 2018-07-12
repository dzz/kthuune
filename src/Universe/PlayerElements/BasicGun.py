from Beagle import API as BGL
from ..RangedEnemyAttacks.BasicProjectile import BasicProjectile
from random import uniform 

class BasicGun():
    clip_size = 20
    cooldown = 5
    accuracy_inverted = 0.2
    reload_time = 45

    def __init__(self,owner):
        self.texture = BGL.assets.get('KT-player/animation/guns')[0]
        self.clip = BasicGun.clip_size
        self.owner = owner
        self.recharge = 0
        self.reset_timer = -1
        self.blocked = False
        self.fireable = True

    def tick(self):
        self.recharge -= 1

        self.reset_timer -= 1
        if self.owner.LB_REL:
            self.blocked = False
            self.reset_timer = BasicGun.reload_time

        if self.reset_timer == 0 and (self.clip < BasicGun.clip_size ):
            self.owner.floor.sounds.play( self.owner.floor.sounds.sfx_reload )
            self.clip = BasicGun.clip_size
        
        if (self.reset_timer<=0) and (self.clip>0) and not(self.blocked):
            self.fireable = True
        else:
            self.fireable = False
            if(self.owner.LB_PRESSED):
               self.owner.floor.sounds.play( self.owner.floor.sounds.sfx_non )
               self.blocked = True

        if(self.recharge<0) and (self.reset_timer<=0) and (self.clip>0) and not(self.blocked):
                if(self.owner.LB_DOWN):
                    self.clip -= 1
                    self.recharge = BasicGun.cooldown
                    projectile = BasicProjectile(animation='bright', override_spd = 0.9, p = list(self.owner.p), rad = self.owner.aim_rad+(uniform(-1.0,1.0)*BasicGun.accuracy_inverted))
                    projectile.vs_enemy = True
                    self.owner.floor.create_object( projectile )
                    self.owner.floor.sounds.play( self.owner.floor.sounds.sfx_bullet )


