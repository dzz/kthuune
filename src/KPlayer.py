from Beagle import API as BGL
from Newfoundland.Object import Object
from Newfoundland.Player import Player
from random import uniform,choice
from math import floor,pi,atan2,sin, hypot

from client.beagle.Newfoundland.GeometryUtils import segments_intersect


def ur1():
    return uniform(0.0,1.0)

class PlayerPhantom(Object):
    def customize(self):
        self.texture = self.player.texture
        self.animation_target = ( self.target.p[0], self.target.p[1] )

        self.p[0] = self.player.p[0]
        self.p[1] = self.player.p[1]

        dx = self.animation_target[0] - self.p[0]
        dy = self.animation_target[1] - self.p[1]

        self.p[0] = self.p[0] - (dx*0.5)
        self.p[1] = self.p[1] - (dy*0.5)

        self.visible = False
        self.buftarget = "floor"
        self.z_index = 900
        self.tick_type = Object.TickTypes.PURGING
        self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
        self.light_radius = 8.0
        self.light_color = [ 0.0,0.0,1.0,1.0 ]
        self.animation_counter = 0
        self.size = [ 3.0,3.0]
    
    def tick(self):
        self.animation_counter = self.animation_counter + 1
        if(self.animation_counter-self.animation_threshold > 12 ):
            self.floor.objects.remove(self)
            return False
        if(self.animation_counter > self.animation_threshold):
            self.visible = True
            dx = (self.animation_target[0] - self.p[0]) / 4
            dy = (self.animation_target[1] - self.p[1]) / 4
            self.p[0] = self.p[0] + dx
            self.p[1] = self.p[1] + dy
        return True
        

class Hud():
    view = BGL.view.widescreen_16_9

class Card():
    shader = BGL.assets.get("KT-player/shader/card")
    primitive = BGL.primitive.unit_uv_square

    def render(self):
        Card.primitive.render_shaded( Card.shader, self.get_shader_params() )

class HeartCard(Card):
    textures = [
            BGL.assets.get('KT-player/texture/heartcard0000'),
            BGL.assets.get('KT-player/texture/heartcard0001')
        ]
    #primitive = BGL.primitive.unit_uv_square
    def __init__(self, player):
        self.fridx = choice( range(0,180) )
        self.player = player

    def tick(self):
        self.fridx = (self.fridx + 1) %180

    def get_shader_params(self):

        return {
            "statusamt" : [ self.player.hp / 100.0 ],
            "statuscolor" : [ 1.0,0.0,0.0,1.0 ],
            "tick" : [ self.player.cardtick ],
            "texBuffer"            : HeartCard.textures[int(self.fridx/90)],
            "translation_local"    : [ 0, 0 ],
            "scale_local"          : [ 1.0*0.4,1.5*0.4],
            "translation_world"    : [ 7.5,-3.75],
            "scale_world"          : [1.0,1.0],
            "view"                 : Hud.view,
            "rotation_local"       : 0.0,
            "filter_color"         : [1.0,1.0,1.0,1.0],
            "uv_translate"         : [ 0,0 ] }

class SwordCard(Card):
    textures = [
            BGL.assets.get('KT-player/texture/swordcard0000'),
            BGL.assets.get('KT-player/texture/swordcard0001')
        ]
    #primitive = BGL.primitive.unit_uv_square
    def __init__(self, player):
        self.fridx = choice( range(0,180) )
        self.player = player

    def tick(self):
        self.fridx = (self.fridx + 1) %180

    def get_shader_params(self):

        return {
            "statusamt" : [ self.player.sword.stamina ],
            "statuscolor" : [ 0.0,1.0,0.0,1.0 ],
            "tick" : [self.player.cardtick+10.0],
            "texBuffer"            : SwordCard.textures[int(self.fridx/90)],
            "translation_local"    : [ 0, 0 ],
            "scale_local"          : [ 1.0*0.4,1.5*0.4],
            "translation_world"    : [ 7.5,-2.5],
            "scale_world"          : [1.0,1.0],
            "view"                 : Hud.view,
            "rotation_local"       : 0.0,
            "filter_color"         : [1.0,1.0,1.0,1.0],
            "uv_translate"         : [ 0,0 ] }

class WandCard(Card):
    textures = [
            BGL.assets.get('KT-player/texture/wandcard0000'),
            BGL.assets.get('KT-player/texture/wandcard0001')
        ]
    #primitive = BGL.primitive.unit_uv_square
    def __init__(self, player):
        self.fridx = choice( range(0,180) )
        self.player = player

    def tick(self):
        self.fridx = (self.fridx + 1) %180

    def get_shader_params(self):

        return {
            "statusamt" : [ 1.0 ],
            "statuscolor" : [ 0.0,0.0,1.0,1.0 ],
            "tick" : [self.player.cardtick+40.0],
            "texBuffer"            : WandCard.textures[int(self.fridx/90)],
            "translation_local"    : [ 0, 0 ],
            "scale_local"          : [ 1.0*0.4,1.5*0.4],
            "translation_world"    : [ 7.5,-1.25],
            "scale_world"          : [1.0,1.0],
            "view"                 : Hud.view,
            "rotation_local"       : 0.0,
            "filter_color"         : [1.0,1.0,1.0,1.0],
            "uv_translate"         : [ 0,0 ] }


def rad_2_index(rad, segments):
    segment_amt = ((2*pi)/segments)
    rad -= (segment_amt*0.5) # center
    rad += pi
    segment = floor((rad/segment_amt)%segments)
    return int(segment)

class Sword(Object):
    STATE_IDLE = 0
    STATE_CHARGING = 1
    STATE_ATTACK_PENDING = 2
    STATE_DISCHARGING = 3
    STATE_AWAITING_RELEASE = 4
    STATE_SPIN_ATTACK = 5

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
        if(self.player.state == KPlayer.STATE_STUNNED ):
            self.state = Sword.STATE_IDLE
            self.visible = False
            return True
        else:
            self.visible = True

        pad = self.player.controllers.get_virtualized_pad( self.player.num )
        btns = BGL.gamepads.buttons

        self.stimer = self.stimer + 1
        if self.state == Sword.STATE_IDLE:
            self.stamina = min(self.stamina * 1.008,1.0)
            self.stimer = 0
            if pad.button_down( btns.RIGHT_BUMPER ):
                if self.stamina > 0.04:
                    self.stamina = self.stamina * 0.83
                    self.state = Sword.STATE_CHARGING
                    self.stimer = 0
                else:
                    self.player.set_state(KPlayer.STATE_STUNNED)

        if self.state == Sword.STATE_CHARGING:
            self.stamina = self.stamina * 0.995
            self.discharge_mod = self.discharge_mod * 1.02
            if not pad.button_down( btns.RIGHT_BUMPER ) or self.stamina < 0.02:
                if(self.stimer > Sword.spin_attack_threshold):
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
                self.player.set_state(KPlayer.STATE_STUNNED)

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

class KPlayer(Player):

    STATE_DEFAULT = 0
    STATE_STUNNED = 1
    STATE_DODGING = 2
    
    def get_crit_mod(self):

        if self.combo_count > 8:
            return 2.8
        if self.sword.state == Sword.STATE_DISCHARGING:
            return 2.1
        else:
            return 1.5

    def receive_ranged_attack(self, attack):
        self.hp = self.hp - attack.attack_str
        self.attack_object = attack
        self.attack_physics_timer = 25 
        self.set_hud_message("YOU GOT HIT!")
        self.link_count = 0
        self.combo_count = 0
        self.combo_reset_cooldown = 0
        self.hurt_flash_timer = 25
        self.sword.state = Sword.STATE_IDLE
        self.sword.stimer = 0
 
    def attempt_snap_attack(self):
        def se_priority(se):
            dx = se.p[0] - self.p[0]
            dy = se.p[1] - self.p[1]
            se.last_priority_score = (dx*dx)+(dy*dy)
            return se.last_priority_score
            

        def can_reach(player, se):
            path = [[ player.p[0], player.p[1] ], [ se.p[0], se.p[1] ]]
            for segment in player.floor.get_light_occluders():
                if(segments_intersect( segment, path)):
                    return False
            return True
            
        sorted_snap_enemies = sorted( self.floor.snap_enemies, key=lambda x:se_priority(x))
        filtered_snap_enemies = list(filter( lambda x: ((x.last_priority_score < 400) and (can_reach(self,x))) or x.last_priority_score<10, sorted_snap_enemies))

        hit = False
        target = None
        for se in filtered_snap_enemies:

            crit = False
            if self.last_link == 0:
                crit = True
            delta = None
            if(se.last_priority_score<10) and (se.snap_type == 1) and (se.iframes in range(1,9)):
                delta = 0
                crit = True
            else:
                dx = se.p[0] - self.p[0]
                dy = se.p[1] - self.p[1]
                rad = atan2(dy,dx)
                
                delta = abs( rad - self.rad )
            if(delta < 0.85):
                self.floor.freeze_frames = 2
                self.floor.freeze_delay = 2

                ##ENEMY snaptype
                if(se.snap_type == 1):
                    se.receive_snap_attack(crit)
                for x in range(0,15):
                    self.floor.create_object( PlayerPhantom( player = self, animation_threshold = 2*x, target = se ) )
                self.p[0] = se.p[0]
                self.p[1] = se.p[1]
                self.sword.state = Sword.STATE_DISCHARGING
                self.sword.stimer = 11 #short circuit the 'snap' window
                self.snap_cooldown = 30
                hit = True
                target = se
                break
            else:
                pass

        if hit:
            self.snap_attack_frozen = True
            self.combo_reset_cooldown = 60*3
            if( se.snap_type == 1 ):
                self.combo_count = self.combo_count + 1
            self.last_link = se.snap_type
            self.link_count = self.link_count + 1
        else:
            self.combo_count = 0
            self.link_count = 0

        
    def set_state(self,state):
        self.stimer = 0
        self.state = state

    def __init__(self, **kwargs):
        #playerinit

        self.snap_attack_frozen = False
        self.attack_physics_timer = 0
        self.snap_cooldown = 0
        self.combo_reset_cooldown = 0
        self.link_count = 0
        self.X_PRESSED = False
        self.X_STATE = [ False, False ]

        self.stimer = 0
        self.state = KPlayer.STATE_DEFAULT
        self.last_link = None
        self.hurt_flash_timer = 0
        overrides =  {
            "light_type" : Object.LightTypes.DYNAMIC_SHADOWCASTER,
            "light_radius" : 45.0,
            "light_color" : [ 0.65,0.45,0.3,1.0],
            "walk_tick" : 0,
            "z_index" : 1,
            "sword_swing" : 0,
            "sword_swing_cooldown" : 20,
            "sword_released" : True,
            "filtered_speed" : 0.0,
            "buftarget" : "popup",
            "snapshot_fields" : [ 'p','hp' ],
            "dir" : [0.0,0.0],
            "color" : [0.0,0.0,0.0,1.0]
        }
        self.set_combat_vars()
        overrides.update(kwargs)
        Player.__init__(self, **overrides)
        self.base_light_color = self.light_color
        KPlayer.swing_textures = [
            BGL.assets.get('KT-player/texture/knight_sword0000'),
            BGL.assets.get('KT-player/texture/knight_sword0001'),
            BGL.assets.get('KT-player/texture/knight_sword0002'),
            BGL.assets.get('KT-player/texture/knight_sword0003'),
            BGL.assets.get('KT-player/texture/knight_sword0004'),
            BGL.assets.get('KT-player/texture/knight_sword0005'),
            BGL.assets.get('KT-player/texture/knight_sword0006'),
            BGL.assets.get('KT-player/texture/knight_sword0007'),
            BGL.assets.get('KT-player/texture/knight_sword0008'),
            BGL.assets.get('KT-player/texture/knight_sword0009'),
            BGL.assets.get('KT-player/texture/knight_sword0010'),
            BGL.assets.get('KT-player/texture/knight_sword0011'),
            BGL.assets.get('KT-player/texture/knight_sword0012'),
            BGL.assets.get('KT-player/texture/knight_sword0013'),
            BGL.assets.get('KT-player/texture/knight_sword0014'),
            BGL.assets.get('KT-player/texture/knight_sword0015'),
            BGL.assets.get('KT-player/texture/knight_sword0016'),
            BGL.assets.get('KT-player/texture/knight_sword0017')
        ]

        KPlayer.textures = [
            BGL.assets.get('KT-player/texture/knight0000'),
            BGL.assets.get('KT-player/texture/knight0001'),
            BGL.assets.get('KT-player/texture/knight0002'),
            BGL.assets.get('KT-player/texture/knight0003'),
            BGL.assets.get('KT-player/texture/knight0004'),
            BGL.assets.get('KT-player/texture/knight0005'),
            BGL.assets.get('KT-player/texture/knight0006'),
            BGL.assets.get('KT-player/texture/knight0007'),
            BGL.assets.get('KT-player/texture/knight0008'),
            BGL.assets.get('KT-player/texture/knight0009'),
            BGL.assets.get('KT-player/texture/knight0010'),
            BGL.assets.get('KT-player/texture/knight0011'),
            BGL.assets.get('KT-player/texture/knight0012'),
            BGL.assets.get('KT-player/texture/knight0013'),
            BGL.assets.get('KT-player/texture/knight0014'),
            BGL.assets.get('KT-player/texture/knight0015'),
            BGL.assets.get('KT-player/texture/knight0016'),
            BGL.assets.get('KT-player/texture/knight0017'),
            BGL.assets.get('KT-player/texture/knight0018'),
            BGL.assets.get('KT-player/texture/knight0019'),
            BGL.assets.get('KT-player/texture/knight0020'),
            BGL.assets.get('KT-player/texture/knight0021'),
            BGL.assets.get('KT-player/texture/knight0022'),
            BGL.assets.get('KT-player/texture/knight0023')
        ]

        self.filtered_speed = self.speed
        self.attacked = False
        self.dash_flash = False
        self.dash_combo = False
        self.hud_buffer = BGL.framebuffer.from_dims(320,240)
        self.combo_count = 0
        self.link_count = 0
        self.can_combo = False
        self.kill_success = False
        self.target_consumed = False
        self.target_cooldown = 0.0
        self.hud_message_timeout = 0.0
        self.hud_message = ""
        self.critical_hit_display_counter = 0


    def set_combat_vars(self):
        self.hp = 100
        self.attack_str = 40
        self.crit_chance = 1.0/5.0
        self.attack_bonus = 0.2
        self.defense = 5

    def get_pad(self):
        pad = self.controllers.get_virtualized_pad( self.num )
        return pad

    def set_hud_message(self, msg, timeout = 400):
        self.hud_message_timeout = timeout
        self.hud_message = msg.upper()

    def notify_crit(self):
        self.critical_hit_display_counter = 60
        self.floor.freeze_frames = 6
        self.floor.freeze_delay = 4

    def render_hud(self):

        with BGL.context.render_target( self.hud_buffer ):
            BGL.context.clear(0.0,0.0,0.0,0.0)
            if(self.critical_hit_display_counter>0) and (self.critical_hit_display_counter<55):
                offsx = choice(range(-1,1))
                offsy = choice(range(-1,1))
                #BGL.lotext.render_text_pixels("CRITICAL", 130-20+offsx,90-20+offsy, [ 1.0,0.0,0.0 ] )
            with BGL.blendmode.alpha_over:
                #BGL.lotext.render_text_pixels("HP:{0}".format(self.hp-1), 130,220,[1.0,0.0,0.0] )
                if(self.combo_count>1):
                    offsx = choice(range(-1,1))
                    offsy = choice(range(-1,1))
                    BGL.lotext.render_text_pixels("COMBO:{0}".format(self.combo_count-1), 4+offsx,4+offsy, [1.0,uniform(0.0,1.0),1.0] )

                if(self.hud_message_timeout>0):
                    mx = 160 - floor(len(self.hud_message)*4)

                    f = 1.0
                    if(self.hud_message_timeout<20):
                        f = self.hud_message_timeout / 100.0;
                        
                    urc = [ ur1()*f,ur1()*f,ur1()*f,1.0 ]
                    urc1 = [ ur1()*0.5*f,ur1()*0.5,ur1()*0.5*f,1.0 ]
                    BGL.lotext.render_text_pixels(self.hud_message, mx-1, 240-11, urc )
                    BGL.lotext.render_text_pixels(self.hud_message, mx, 240-10, urc1 )

        with BGL.blendmode.alpha_over:
            self.hud_buffer.render_processed( BGL.assets.get("beagle-2d/shader/passthru") )
            self.floor.render_objects("hud")


        self.heartcard.render()
        self.swordcard.render()
        self.wandcard.render()



    def customize(self):
        self.heartcard = HeartCard(self)
        self.swordcard = SwordCard(self)
        self.wandcard = WandCard(self)
        #self.hp = 100
        self.dash_amt = 1.0
        self.sword = Sword(player=self)
        self.pumped_dashcombo = False
        self.can_backstep = True
        self.backstep_cooldown = -5
        self.backstepping = False
        self.cardtick = 0.0
        self.attack_object = None
    
    def link_floor(self):
        self.floor.create_object( self.sword )

    def get_shader_params(self):
        base_params = Player.get_shader_params(self)
        if self.hp > 0:
            base_params["rotation_local"] = 0.0

        #if self.state == KPlayer.STATE_STUNNED:
        #    base_params["rotation_local"] = sin(self.cardtick)*0.2


        return base_params
        

    def determine_texture(self):

        modamt = 1
        if self.dash_flash:
            modamt = modamt*3

        if self.sword_swing == 0:
            tex = KPlayer.textures[4]

            yidx = 0
            if(self.rad > 0):
                yidx = 3
            idx = rad_2_index(self.rad,8)*3
            widx = (self.walk_tick*modamt//40) % 4
            woffs = [ 0,1,0,2 ]
            tex = KPlayer.textures[idx+woffs[widx]]
            return tex
        else:
            idx = rad_2_index(self.rad,6)*3

            offs = self.sword_swing_cooldown - self.sword_swing
            offs = int(floor(3*(offs/self.sword_swing_cooldown)))

            idx = idx + offs
            tex = KPlayer.swing_textures[idx]
            return tex
 
    def enemy_attack(self,damage):

        if self.sword.state == Sword.STATE_CHARGING:
            return
        if self.sword.state == Sword.STATE_ATTACK_PENDING:
            return


    def is_dashing(self):
        return self.dash_combo

    def notify_succesful_attack(self):
        pass

    def next_dashcombo(self):
        pass

    def pump_dashcombo(self):
        pass


    def notify_enemy_killed(self):
        self.kill_success = True
        pass

    def deal_with_buttons(self,pad):

        self.X_STATE[0] = self.X_STATE[1]
        self.X_STATE[1] = pad.button_down( BGL.gamepads.buttons.X )
    
        if self.X_STATE[1] is True and self.X_STATE[0] is False:
            self.X_PRESSED = True
        else:
            self.X_PRESSED = False

        if self.X_STATE[1] is False:
            self.snap_attack_frozen = False

    def tick(self):
        #player tick

        if(self.combo_reset_cooldown>0):
            self.combo_reset_cooldown = self.combo_reset_cooldown - 1
        else:
            self.combo_count = 0
            self.link_count = 0
            self.last_link = None

        self.critical_hit_display_counter = self.critical_hit_display_counter - 1
        self.snap_cooldown = self.snap_cooldown - 1
        self.hud_message_timeout = self.hud_message_timeout - 1
        self.stimer = self.stimer + 1
        self.cardtick = self.cardtick + 0.01
        self.heartcard.tick()
        self.swordcard.tick()
        self.wandcard.tick()

        self.pumped_dashcombo = False
        if(self.hp < 0 ):
            self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
            self.light_color = [ 1.0,0.0,0.0,1.0]
            self.light_radius = 100
            self.texture = BGL.assets.get('KT-player/texture/skeleton')
            self.size = [2.0,2.0]
            self.rad = atan2(self.p[0]-self.snapshot['p'][0],self.p[1]-self.snapshot['p'][1])
            return True
        pad = self.controllers.get_virtualized_pad( self.num )
        self.deal_with_buttons(pad)

        if (self.X_PRESSED and self.link_count>0) or ( (self.sword.state == Sword.STATE_DISCHARGING) and (self.sword.stimer == 10)):
            self.attempt_snap_attack()

        self.light_color = self.base_light_color
        
        if(abs(pad.left_stick[0])>0.003) or (abs(pad.left_stick[1])>0.003):
            self.walk_tick = self.walk_tick+1
            if(self.walk_tick>400):
                self.walk_tick = 0
        else:
            self.walk_tick = 0
 
        if(self.state == KPlayer.STATE_STUNNED ):
            self.v[0] = self.v[0] * 0.2
            self.v[1] = self.v[1] * 0.2

            #if(self.attack_object):
            #    self.v[0] = self.v[0] + (self.attack_object.v[0]*4)
            #    self.v[1] = self.v[1] + (self.attack_object.v[1]*4)

            if self.stimer > 15:
                self.attack_object = None
                self.set_state( KPlayer.STATE_DEFAULT )

        if(self.state == KPlayer.STATE_DODGING ):
            self.v[0] = self.dv[0] * 4
            self.v[1] = self.dv[1] * 4

            if(self.sword.state is not Sword.STATE_IDLE):
                self.set_state(KPlayer.STATE_DEFAULT)
            if(self.stimer > 9 ):
                self.set_state(KPlayer.STATE_DEFAULT)

        if(self.state == KPlayer.STATE_DEFAULT ):
            if not pad.button_down( BGL.gamepads.buttons.B ):
                self.can_backstep = True

            if(pad.button_down( BGL.gamepads.buttons.B ) and self.can_backstep and self.sword.state == Sword.STATE_IDLE):
                if(self.stimer > 30 ):
                    delta = [ pad.left_stick[0] , pad.left_stick[1]  ]
                    self.dv = [ delta[0] * self.speed, delta[1] * self.speed ]
                    self.can_backstep = False
                    self.set_state(KPlayer.STATE_DODGING)


            calc_speed = self.speed

            self.dash_flash = False
            if(self.sword.state == Sword.STATE_CHARGING):
                calc_speed = self.speed * 0.5

            if(self.sword.state == Sword.STATE_DISCHARGING):
                self.dash_flash = True
                calc_speed = self.speed * 4.0

            if(self.sword.state == Sword.STATE_ATTACK_PENDING):
                self.dash_flash = True
                calc_speed = self.speed * 0.001

            if(self.aiming_beam.aiming):
                calc_speed = calc_speed * 0.5

            self.filtered_speed = (self.filtered_speed*0.8) + (calc_speed*0.2)
            calc_speed = self.filtered_speed
            Object.tick(self)
            pad = self.controllers.get_virtualized_pad( self.num )

            delta = [ pad.left_stick[0] * calc_speed, pad.left_stick[1] * calc_speed ]
            self.v[0] = self.v[0]*0.8+delta[0]*0.2
            self.v[1] = self.v[1]*0.8+delta[1]*0.2

            self.rad = atan2( self.v[1], self.v[0] )
            self.light_radius = 15.0
            self.light_color = self.base_light_color
            impulse = uniform(5.0,35.0)
            self.light_radius = (self.light_radius*0.96) + (impulse*0.04)
            self.texture = self.determine_texture()

            if(self.dash_flash):
                rc = uniform(0.0,1.0)
                self.light_color= [rc,rc,rc,1.0]
    
            if(self.sword.state == Sword.STATE_CHARGING):
                self.light_color = [ 1.0,1.0,1.0,1.0 ]
                self.light_radius = uniform(0.0,100.0)
            if(self.sword.state == Sword.STATE_ATTACK_PENDING):
                self.light_color = [ uniform(0.0,1.0),uniform(0.0,1.0),0.0,1.0 ]
                self.light_radius = uniform(1.0,250.0)
            if(self.sword.state == Sword.STATE_DISCHARGING):
                self.light_color = [ 0.0,uniform(0.0,1.0),uniform(0.0,1.0),1.0]
                self.light_radius = uniform(40.0,50.0)


            if(self.snap_cooldown>0):
                self.v[0] = 0
                self.v[1] = 0
            

            if(self.snap_attack_frozen):
                self.v[0] = 0
                self.v[1] = 0 

            if(self.attack_physics_timer>0):

                print("TRYING TO APPLY ATTACK REBOUND")
                self.attack_physics_timer = self.attack_physics_timer - 1

                print(self.attack_object.v)
                self.v[0] = (self.v[0]*0.2) + (self.attack_object.vx*2)
                self.v[1] = (self.v[1]*0.2) + (self.attack_object.vy*2)
            else:
                self.attack_object = None


            if(self.hurt_flash_timer>0):
                self.color = [1.0,0.0,0.0,1.0]
                self.hurt_flash_timer -= 1
            elif(self.link_count>0):
                    self.color = [1.0,1.0,0.7,1.0]
            else:
                self.color = [1.0,1.0,1.0,1.0]
        
            Object.tick(self)

