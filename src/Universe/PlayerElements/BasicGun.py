from Beagle import API as BGL
from ..RangedEnemyAttacks.BasicProjectile import BasicProjectile
from random import uniform 

class BasicGun():

    FORCE = 0
    LIGHTNING = 1
    SEEK = 2
    EXPLO = 3

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

        self.slot1 = BasicGun.FORCE
        self.slot2 = BasicGun.LIGHTNING

    def cycle_1(self):
       self.slot1 += 1
       if(self.slot1>3):
           self.slot1 = 0

    def cycle_2(self):
        if self.slot2 == None:
            self.slot2 = 0
        else:
            self.slot2 += 1
            if(self.slot2>3):
                self.slot2 = None
            
    def determine_bullet_animation(self):

        if(self.slot2 == None):
            self.bullet_anim_id = self.slot1+3
        else:
            has_force = (self.slot1 == BasicGun.FORCE) or (self.slot2 == BasicGun.FORCE)
            has_light = (self.slot1 == BasicGun.LIGHTNING) or (self.slot2 == BasicGun.LIGHTNING)
            has_seek = (self.slot1 == BasicGun.SEEK) or (self.slot2 == BasicGun.SEEK)
            has_explo = (self.slot1 == BasicGun.EXPLO) or (self.slot2 == BasicGun.EXPLO)

            if(self.slot1==self.slot2):
                if has_force:
                    self.bullet_anim_id = self.slot1+3
                if has_light:
                    self.bullet_anim_id = self.slot1+3
                if has_seek:
                    self.bullet_anim_id = self.slot1+3
                if has_explo:
                    self.bullet_anim_id = self.slot1+3
            else:
                if has_force and has_light:
                    self.bullet_anim_id = 7
                if has_force and has_seek:
                    self.bullet_anim_id = self.slot1+3
                if has_force and has_explo:
                    self.bullet_anim_id = 8
                if has_light and has_seek:
                    self.bullet_anim_id = 9
                if has_light and has_explo:
                    self.bullet_anim_id = 10
                if has_seek and has_explo:
                    self.bullet_anim_id = 11

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

        self.determine_bullet_animation()#todo: lazy calculate
        if(self.recharge<0) and (self.reset_timer<=0) and (self.clip>0) and not(self.blocked):
                if(self.owner.LB_DOWN):
                    self.clip -= 1
                    self.recharge = BasicGun.cooldown
                    projectile = BasicProjectile(animation=self.bullet_anim_id, override_spd = 0.9, p = list(self.owner.p), rad = self.owner.aim_rad+(uniform(-1.0,1.0)*BasicGun.accuracy_inverted))
                    projectile.vs_enemy = True
                    self.owner.floor.create_object( projectile )
                    self.owner.floor.sounds.play( self.owner.floor.sounds.sfx_bullet )


