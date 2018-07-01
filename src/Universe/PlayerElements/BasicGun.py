from ..RangedEnemyAttacks.BasicProjectile import BasicProjectile

class BasicGun():
    def __init__(self,owner):
        self.owner = owner
        self.recharge = 0

    def tick(self):
        self.recharge -= 1

        if(self.recharge<0):
            if(self.owner.LB_DOWN):
                self.recharge = 10
                projectile = BasicProjectile(animation='bright', override_spd = 0.9, p = list(self.owner.p), rad = self.owner.aim_rad)
                projectile.vs_enemy = True
                self.owner.floor.create_object( projectile )

        pass
