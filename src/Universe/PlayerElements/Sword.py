from Beagle import API as BGL
from Newfoundland.Object import Object
from math import sin
from random import uniform
from ...Abilities import Abilities

class Sword(Object):
    STATE_IDLE = 0
    STATE_CHARGING = 1
    STATE_ATTACK_PENDING = 2
    STATE_DISCHARGING = 3
    STATE_AWAITING_RELEASE = 4
    STATE_SPIN_ATTACK = 5

    #creepy pasta because circ ref
    KPLAYER_STATE_DEFAULT = 0
    KPLAYER_STATE_STUNNED = 1
    KPLAYER_STATE_DODGING = 2
    KPLAYER_STATE_FIRING = 3

    max_charge = 40
    max_pending = 60
    max_discharge = 10
    spin_attack_threshold = 0
    max_spin_attack = 15

    def __init__(self,**kwargs):
        Object.__init__(self,**kwargs)

    def customize(self):
        self.tick_type = Object.TickTypes.TICK_FOREVER
        self.texture = BGL.assets.get('KT-player/texture/sword')
        self.buftarget = "popup"
        self.z_index = 1
        self.bob_index = 0.0
        self.collected = True
        self.state = Sword.STATE_IDLE
        self.stimer = 0.0
        self.discharge_mod = 1.0
        self.stamina = 1.0



    def tick(self):

        self.visible = Abilities.Sword and not self.floor.player.slash.visible and self.floor.player.visible and self.floor.player.slash.cooldown<=0

        if not self.visible:
            return True

        if(self.player.state == Sword.KPLAYER_STATE_STUNNED ):
            self.state = Sword.STATE_IDLE
            #self.visible = False
            return True
        else:
            pass
            #self.visible = True

        pad = self.player.controllers.get_virtualized_pad( self.player.num )
        btns = BGL.gamepads.buttons

        self.stimer = self.stimer + 1
        if self.state == Sword.STATE_IDLE:
            self.stamina = min(self.stamina * 1.008,1.0)
            self.stimer = 0
            if pad.button_down( btns.RIGHT_BUMPER ) and False:
                if self.stamina > 0.04:
                    self.stamina = self.stamina * 0.83
                    self.state = Sword.STATE_CHARGING
                    self.stimer = 0
                    KSounds.play( KSounds.charge_initiated )
                else:
                    self.player.set_state(Sword.KPLAYER_STATE_STUNNED)

        if self.state == Sword.STATE_CHARGING:
            self.stamina = self.stamina * 0.995
            self.discharge_mod = self.discharge_mod * 1.02
            if not pad.button_down( btns.RIGHT_BUMPER ) or self.stamina < 0.02:
                if(self.stimer > Sword.spin_attack_threshold):
                    KSounds.play(KSounds.charge_executed)
                    self.state = Sword.STATE_DISCHARGING
                    self.stimer = 0
                else:
                    self.state = Sword.STATE_SPIN_ATTACK
                    self.stimer = 0
            if self.stimer >= Sword.max_charge:
                self.state = Sword.STATE_ATTACK_PENDING
                self.stimer = 0

        if self.state == Sword.STATE_ATTACK_PENDING:
            self.stamina = self.stamina *0.992
            if self.stamina < 0.02:
                self.player.set_state(Sword.KPLAYER_STATE_STUNNED)

            if self.stimer >= Sword.max_pending or (not pad.button_down(btns.RIGHT_BUMPER)):
                self.stimer = 0
                self.state = Sword.STATE_DISCHARGING

        if self.state == Sword.STATE_DISCHARGING:
            if self.stimer >= (Sword.max_discharge * self.discharge_mod):
                self.stimer = 0
                self.state = Sword.STATE_AWAITING_RELEASE

        if self.state == Sword.STATE_AWAITING_RELEASE:
            self.discharge_mod = 1.0
            if not pad.button_down( btns.RIGHT_BUMPER):
                self.state = Sword.STATE_IDLE

        if self.state == Sword.STATE_SPIN_ATTACK:
            if(self.stimer > Sword.max_spin_attack):
                self.state = Sword.STATE_AWAITING_RELEASE
            

        if not self.collected:
            if hypot( self.p[0]-self.player.p[0],self.p[1]-self.player.p[1]) < 1.5:
                self.collected = True
            return

        self.bob_index = self.bob_index + 0.04
        self.p[0] = self.player.p[0]
        self.p[1] = self.player.p[1]+0.001

        self.size = [1.0,1.0]

        if self.state == Sword.STATE_IDLE or self.state == Sword.STATE_AWAITING_RELEASE:
            bob = sin(self.bob_index)
            if(self.player.rad >= 0.0): self.rad = (-2.9-3.14) + (0.1*bob)
            if(self.player.rad < 0.0): self.rad = (2.7) - (0.1*bob)
            if(self.player.rad > 0.0): self.z_index = 1
            if(self.player.rad < 0.0): self.z_index = 0

        if self.state == Sword.STATE_SPIN_ATTACK:
            nchrg = self.stimer / self.max_spin_attack
            self.rad = (-4.2) + (6.28*nchrg)

        if self.state == Sword.STATE_CHARGING:
            nchrg = self.stimer / self.max_charge
            self.rad = -(4.2)+(4.2*(nchrg*nchrg*nchrg))

        if self.state == Sword.STATE_ATTACK_PENDING:
            self.rad = 3.14+1.07 + uniform(-0.2,0.2)
            self.z_index = 2
            self.size = [1.5,1.5]

        if self.state == Sword.STATE_DISCHARGING:
            self.rad = self.player.rad
            self.size = [1.7,1.0]

    def get_shader_params(self):
        bp = Object.get_shader_params(self)
        bp['translation_local'][0] = 1.1
        bp['translation_local'][1] = 0.1
        return bp
