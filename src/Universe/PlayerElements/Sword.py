from Beagle import API as BGL
from Newfoundland.Object import Object
from math import sin,cos
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

        self.visible = Abilities.Sword and not self.floor.player.throw_sword_attack.visible and self.floor.player.visible and self.floor.player.throw_sword_attack.cooldown<=0

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

        self.bob_index = self.bob_index + 0.4
        self.p[0] = self.player.p[0] + (cos(self.player.rad-1.57)*0.6)
        self.p[1] = (self.player.p[1] + (sin(self.player.rad-1.57)*0.2)) - 2.0
        self.rad = -1.57
        self.size = [0.8,0.8]

    def get_shader_params(self):
        bp = Object.get_shader_params(self)
        bp["translation_local"][1] = 0.0
        bp["translation_local"][0] += 0.1*sin(self.bob_index)
        bp["scale_local"][1] *= -1.0
        #bp["translation_local"][1] -= 0.0
        bp["filter_color"] = [ 0.0,0.0,0.0,0.0 ]
        return bp

