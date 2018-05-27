#####
##
#
# OH, IT'S YOU.
# I'LL ADMIT, I'M SURPRISED YOU MADE IT THIS FAR.
#
#
import audio

from Beagle import API as BGL
from Newfoundland.Object import Object
from Newfoundland.Player import Player
from random import uniform,choice
from math import floor,pi,atan2,sin, hypot,cos
from .Abilities import Abilities

from client.beagle.Newfoundland.GeometryUtils import segments_intersect

from .KSounds import KSounds
from .TitleCard import TitleCard

from .WorldMap import WorldMap
from .Universe.LevelEffects.PlayerPhantom import PlayerPhantom
from .Universe.LevelEffects.Dust import Dust
from .Universe.LevelEffects.Explosion import Explosion
from .Universe.PlayerElements.DMMessage import DMMessage
from .Universe.PlayerElements.SlashEffect import SlashEffect
from .Universe.PlayerElements.HealthBubble import HealthBubble
from .Universe.PlayerElements.Sword import Sword
from .Universe.PlayerElements.PlayerInvSlot import PlayerInvSlot
from .Universe.PlayerElements.Hud import Hud
from .Universe.PlayerElements.Cooldowns import Cooldown,SwordCooldown,TelekineCooldown
from .Universe.PlayerElements.TerminalRenderer import TerminalRenderer
from .Universe.PlayerElements.StatusCards import HeartCard, TelekineCard, WandCard, PotionCard, SwordCard
from .Universe.PlayerElements.PotionCountView import PotionCountView
from .Universe.Particles.SplatterParticle import SplatterParticle
from .Universe.Particles.Bird import Bird

## maybe copy this music...
#
# https://youtu.be/R8szhcVlM8g?t=644

def rad_2_index(rad, segments):
    segment_amt = ((2*pi)/segments)
    rad -= (segment_amt*0.5) # center
    rad += pi
    segment = floor((rad/segment_amt)%segments)
    return int(segment)


class KPlayer(Player):
    rainbow = [ 
        [ 148/256, 0.0, 211/256, 1.0 ],
        [ 75/256, 0.0, 130.0/256, 1.0 ],
        [ 0.0, 0.0, 256/256, 1.0 ],
        [ 255/256, 255/256, 0.0, 1.0 ],
        [ 255/256, 127, 0.0, 1.0 ]
    ]
    vl2d_walksword = BGL.assets.get("KT-player/animation/vl2d_walksword")
    vl3d_run = BGL.assets.get("KT-player/animation/vl3d_run")
    vl3d_walk = BGL.assets.get("KT-player/animation/vl3d_walk")
    vl3d_idle = BGL.assets.get("KT-player/animation/vl3d_idle")
    vl3d_sword = BGL.assets.get("KT-player/animation/vl3d_sword")
    vl3d_hit = BGL.assets.get("KT-player/animation/vl3d_hit")

    vl2d_walk = BGL.assets.get("KT-player/animation/vl2d_walk")
    vl2d_idle = BGL.assets.get("KT-player/animation/vl2d_idle")

    BirdmanTick = 0
    BirdmanTextures = [
        BGL.assets.get("KT-player/texture/birdman0000"),
        BGL.assets.get("KT-player/texture/birdman0001"),
        BGL.assets.get("KT-player/texture/birdman0002")
    ]
    ComboSecs = 1.5
    STATE_DEFAULT = 0
    STATE_STUNNED = 1
    STATE_DODGING = 2
    STATE_FIRING = 3
    
    def boost_run_stamina(self):
        self.run_stamina += 25
        if(self.run_stamina>100):
            self.run_stamina = 100 

    def add_time(self,amt):
            self.got_time = 15
            self.life_timer += amt*60
            self.floor.sounds.play(self.floor.sounds.time_totem)

    def has_inv(self):
        for x in self.inventory:
            if x is None:
                return True

    def add_inv(self,inv):
        if(inv=="hp_vial"):
            self.hp += 50
            self.hp = min(self.hp,100)
            self.health_count += 1
        #for i, o in enumerate(self.inventory):
        #    if o is None:
        #        self.inventory[i] = inv
        #        return

    def consume_hp(self):

        if(self.health_count==0):
            return

        self.health_count -= 1
        self.potionFlash = 1.0
        self.ability_timeout = 65
        self.active_ability = KPlayer.ABILITY_HP

        KSounds.play(KSounds.health)
        self.hp = self.hp + 15
        if(self.hp>100):
            self.hp = 100
        pass

    def get_crit_mod(self):

        if self.combo_count > 8:
            return 2.8
        if self.sword.state == Sword.STATE_DISCHARGING:
            return 2.1
        else:
            return 1.5

    def receive_ranged_attack(self, attack):

        if self.shield_frames>0:
            self.floor.create_object( Explosion( p = list(attack.p) ) )
            return

        if self.floor.camera.cinema_target:
            return

        if(self.invuln_frames>0):
            return 
        self.snap_cooldown = 10
        self.hp = self.hp - (attack.attack_str*1.6)
        self.flash_color = [ 1.0,0.0,0.0,1.0 ]
        self.attack_object = attack
        self.attack_physics_timer = 25 
        #self.add_dm_message("You were injured")
        self.link_count = 0
        self.combo_count = 0
        self.combo_reset_cooldown = 0
        self.hurt_flash_timer = 25
        self.sword.state = Sword.STATE_IDLE
        self.sword.stimer = 0
        KSounds.play( KSounds.player_hurt )
        self.pump_timer("injured")
        self.run_animation_alt = 2
        self.run_animation_subtick = 0
 
    def attempt_snap_attack(self, snap = True):

        self.telekineFlash = 1.0
        #teleportCost = 10.0
        teleportCost = 20
        if(self.teleportAmt<teleportCost):
            self.floor.sounds.play(self.floor.sounds.tk_fail)
            return

        self.teleportAmt -= teleportCost

        if not Abilities.Telekine:
            return

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

        filtered_snap_enemies = list(filter( lambda x: ((x.last_priority_score < 550) and (can_reach(self,x))) or x.last_priority_score<10, sorted_snap_enemies))
        filtered_snap_enemies = sorted( filtered_snap_enemies, key=lambda x:2.0-x.snap_type) #prioritize non totems

        self.hittable_hilight= filtered_snap_enemies
        self.hittable_hint_impulse = 1.0

        hit = False
        target = None
        for se in filtered_snap_enemies:

            crit = False
            if self.last_link == 0:
                crit = True

            if (self.run_stamina>10) and self.running:
                crit = True
                
            delta = None
            if(se.last_priority_score<9) and (se.snap_type == 1) and (se.iframes in range(3,10)):
                delta = 0
                crit = True
            else:
                dx = se.p[0] - self.p[0]
                dy = se.p[1] - self.p[1]
                rad = atan2(dy,dx)
                
                delta = abs( rad - self.rad )

            tolerance = (pi*2)/10.25
            if(delta < tolerance) or (delta > ((2*pi)-(tolerance))):
                self.floor.freeze_frames = 2
                self.floor.freeze_delay = 2

                ##ENEMY snaptype
                s2count = 0
                if(se.snap_type == 1):
                    se.receive_snap_attack(crit)

                    for se2 in self.floor.snap_enemies:
                        if(crit and (s2count>4)):
                            break
                        elif s2count>2:
                            break
                        if se2 is se:
                            continue
                        if se2.snap_type == 1:
                            if se2.triggered:
                                dx = se2.p[0] - se.p[0]
                                dy = se2.p[1] - se.p[1]
                                ad = abs(dx)+abs(dy)
                                if ad < 2:
                                    s2count += 1
                                    se2.receive_snap_attack(crit)
                        
                    if crit:
                        KSounds.play( KSounds.crit )
                for x in range(0,15):
                    self.floor.create_object( PlayerPhantom( player = self, animation_threshold = 2*x, target = se ) )

                self.pump_timer('totem')
                self.display_p = [ self.p[0], self.p[1] ]
                if snap:
                    self.p[0] = se.p[0]
                    self.p[1] = se.p[1]
                else:
                    if se.snap_type == 1:
                        tmp = [ se.p[0],se.p[1] ]
                        se.p[0] = self.p[0]
                        se.p[1] = self.p[1]
                        self.p[0] = tmp[0]
                        self.p[1] = tmp[1]
                    if se.snap_type == 0:
                        self.p[0] = se.p[0]
                        self.p[1] = se.p[1]
            
                    
                    
                self.sword.state = Sword.STATE_DISCHARGING
                self.sword.stimer = 11 #short circuit the 'snap' window
                self.snap_cooldown = 7
                hit = True
                target = se
                break
            else:
                self.floor.sounds.play(self.floor.sounds.tk_fail)
                pass

        if hit:
            self.snap_attack_frozen = True
            self.combo_reset_cooldown = 60*KPlayer.ComboSecs
            if( se.snap_type == 1 ):

                #self.add_dm_message("You executed a violent Telekine") 
                self.invuln_frames = 9
                self.snap_animation_buffer = min((1+self.combo_count)*9,22)
                self.combo_count = self.combo_count + 1
                KSounds.play( KSounds.basic_hit )

                if(self.combo_count == 2):
                    KSounds.play( KSounds.groovy )
                if(self.combo_count == 4):
                    KSounds.play( KSounds.groovy )
                if(self.combo_count == 5):
                    KSounds.play( KSounds.tubular )
                if(self.combo_count > 7):
                    KSounds.play( KSounds.tubular )
            else:
                #self.add_dm_message("You executed a passive Telekine") 
                se.sleep_totem( self )
                self.snap_animation_buffer = 6

            self.last_link = se.snap_type
            self.link_count = self.link_count + 1
            KSounds.play( KSounds.snap_landed )
            KSounds.play( choice( [ KSounds.taking_off, KSounds.taking_off2 ] ))
                        
        else:
            self.combo_count = 0
            self.link_count = 0

        
    ABILITY_HP = 0

    def set_state(self,state):
        self.stimer = 0
        self.state = state

    def pump_timer(self,key):
        pass
        #if key=='skeline':
        #    self.life_timer += 450
        #if key=='chargeplate':
        #    self.life_timer += 300
        #if key=='totem':
        #    self.life_timer += 20
        #if key=="completion":
        #    self.life_timer += floor(self.completion_bonus)
        #    self.completion_bonus *= 1.08
        #if key=="death":
        #    self.life_timer -= 500
        #    self.completion_bonus*= 0.9
        #if key=="injured":
        #    self.life_timer -= 75


    def add_sequence_kill(self):
        self.sequence_kills+=1

    def __init__(self, **kwargs):
        #playerinit
        #PLAYER INIT
        #player init
        
        self.rainbow_val = 0
        self.in_editor = False
        self.run_animation_alt = 0
        self.invisible_frames = 0  
        self.got_time = 0
        self.subtick = 0
        self.run_animation_subtick = 0
        self.total_points = 0
        self.suspend_time_penalty = False
        self.violentally_executed_self = False
        self.shield_frames = 0 
        self.sequence_kills = 0
        self.life_timer = 2800
        self.time_penalty = 100
        self.disp_life_timer = self.life_timer
        self.completion_bonus = 900
        self.lt_tick = 0
        self.current_system = "Oort Cloud"
        self.teleportAmt = 100.0
        self.world_map = WorldMap
        self.snap_attack_frozen = False
        self.attack_physics_timer = 0
        self.snap_cooldown = 0
        self.combo_reset_cooldown = 0
        self.link_count = 0
        self.invuln_frames = 0
        self.X_PRESSED = False
        self.X_STATE = [ False, False ]
        self.A_PRESSED = False
        self.A_STATE = [ False, False ]
        self.B_PRESSED = False
        self.B_STATE = [ False, False ]
        self.Y_PRESSED = False
        self.Y_STATE = [ False, False ]

        self.LEFT_STATE = [ False, False ]
        self.LEFT_PRESSED = False
        self.RIGHT_STATE = [ False, False ]
        self.RIGHT_PRESSED = False
        self.UP_STATE = [ False, False ]
        self.UP_PRESSED = False
        self.DOWN_STATE = [ False, False ]
        self.DOWN_PRESSED = False

        self.stimer = 0
        self.state = KPlayer.STATE_DEFAULT
        self.last_link = None
        self.hurt_flash_timer = 0
        self.flash_color = [ 0.0,0.0,0.0,0.0 ]

        self.ability_timeout = 0
        self.active_ability = -1

        self.run_stamina = 100.0

        overrides =  {
            "light_type" : Object.LightTypes.DYNAMIC_SHADOWCASTER,
            "light_radius" : 15.0,
            "light_color" : [ 1.0,1.0,1.0,1.0],
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

        self.physics["radius"] = 1.65
        self.base_light_color = self.light_color

        KPlayer.textures = BGL.assets.get('KT-player/animation/knight')
        KPlayer.swing_textures = BGL.assets.get('KT-player/animation/knight_sword')

        #KPlayer.swing_textures = [
        #    BGL.assets.get('KT-player/texture/knight_sword0000'),
        #    BGL.assets.get('KT-player/texture/knight_sword0001'),
        #    BGL.assets.get('KT-player/texture/knight_sword0002'),
        #    BGL.assets.get('KT-player/texture/knight_sword0003'),
        #    BGL.assets.get('KT-player/texture/knight_sword0004'),
        #    BGL.assets.get('KT-player/texture/knight_sword0005'),
        #    BGL.assets.get('KT-player/texture/knight_sword0006'),
        #    BGL.assets.get('KT-player/texture/knight_sword0007'),
        #    BGL.assets.get('KT-player/texture/knight_sword0008'),
        #    BGL.assets.get('KT-player/texture/knight_sword0009'),
        #    BGL.assets.get('KT-player/texture/knight_sword0010'),
        #    BGL.assets.get('KT-player/texture/knight_sword0011'),
        #    BGL.assets.get('KT-player/texture/knight_sword0012'),
        #    BGL.assets.get('KT-player/texture/knight_sword0013'),
        #    BGL.assets.get('KT-player/texture/knight_sword0014'),
        #    BGL.assets.get('KT-player/texture/knight_sword0015'),
        #    BGL.assets.get('KT-player/texture/knight_sword0016'),
        #    BGL.assets.get('KT-player/texture/knight_sword0017')
        #]

        #KPlayer.textures = [
        #    BGL.assets.get('KT-player/texture/knight0000'),
        #    BGL.assets.get('KT-player/texture/knight0001'),
        #    BGL.assets.get('KT-player/texture/knight0002'),
        #    BGL.assets.get('KT-player/texture/knight0003'),
        #    BGL.assets.get('KT-player/texture/knight0004'),
        #    BGL.assets.get('KT-player/texture/knight0005'),
        #    BGL.assets.get('KT-player/texture/knight0006'),
        #    BGL.assets.get('KT-player/texture/knight0007'),
        #    BGL.assets.get('KT-player/texture/knight0008'),
        #    BGL.assets.get('KT-player/texture/knight0009'),
        #    BGL.assets.get('KT-player/texture/knight0010'),
        #    BGL.assets.get('KT-player/texture/knight0011'),
        #    BGL.assets.get('KT-player/texture/knight0012'),
        #    BGL.assets.get('KT-player/texture/knight0013'),
        #    BGL.assets.get('KT-player/texture/knight0014'),
        #    BGL.assets.get('KT-player/texture/knight0015'),
        #    BGL.assets.get('KT-player/texture/knight0016'),
        #    BGL.assets.get('KT-player/texture/knight0017'),
        #    BGL.assets.get('KT-player/texture/knight0018'),
        #    BGL.assets.get('KT-player/texture/knight0019'),
        #    BGL.assets.get('KT-player/texture/knight0020'),
        #    BGL.assets.get('KT-player/texture/knight0021'),
        #    BGL.assets.get('KT-player/texture/knight0022'),
        #    BGL.assets.get('KT-player/texture/knight0023')
        #]

        self.filtered_speed = self.speed
        self.attacked = False
        self.dash_flash = False
        self.dash_combo = False
        self.hud_buffer = BGL.framebuffer.from_dims(1920,1080)
        self.time_buffer = BGL.framebuffer.from_dims( 160, 120 )
        self.combo_count = 0
        self.link_count = 0
        self.can_combo = False
        self.kill_success = False
        self.target_consumed = False
        self.target_cooldown = 0.0
        self.hud_message_timeout = 0.0
        self.hud_message = ""
        self.critical_hit_display_counter = 0
        self.title_card = TitleCard()
        self.dm_messages = []
        self.dm_msg_cooldown = 0

    def add_dm_message(self, message):
        self.dm_messages.append( DMMessage(message))
        self.dm_messages = self.dm_messages[-9:]
        self.dm_msg_cooldown = 0

    def impulse_hittables(self):
        self.hittable_hint_impulse = 0.5
        self.hittable_hint_real += 0.2

    def add_firefly(self):
        self.hittable_hint_real += 0.01
        self.hittable_hint_impulse = 0.7
        self.flash_color = KPlayer.rainbow[self.rainbow_val]
        self.rainbow_val = (self.rainbow_val+1)%len(KPlayer.rainbow)

        fireflyTeleportBonus = 10.0/12.0
        self.teleportAmt += fireflyTeleportBonus
        KSounds.play( KSounds.firefly )


    def deq_dm_message(self):
        self.dm_messages = self.dm_messages[1:] 

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

    def render_hud(self, render_titlecard = True):
        def ur1():
            return uniform(0.0,1.0)

        with BGL.context.render_target( self.time_buffer ):
            BGL.context.clear(0.0,0.0,0.0,0.0)
            if self.floor.genocide_enabled:
                with BGL.blendmode.alpha_over:
                    #if(self.floor.playing_genocide()):
                    #    BGL.lotext.render_text_pixels("CLEAR THE INFECTION".format(self.disp_life_timer), 20,2,[1.0,1.0,0.0] )
                    #else:
                    #    BGL.lotext.render_text_pixels("FIND THE SWITCHES".format(self.disp_life_timer), 20,2,[1.0,1.0,0.0] )
                    x = (60-self.subtick) / 60.0
                    nstr = "{0}s".format(self.disp_life_timer)
                    cx = 80 - (len(nstr)//2*8)
                    BGL.lotext.render_text_pixels(nstr, cx,102,[0.0,0.0,0.0] )

                    if(self.got_time>0):
                        _ca = uniform(0.0,1.0)
                        _cb = uniform(0.0,1.0)
                        BGL.lotext.render_text_pixels(nstr, cx-1,103,[_ca,_cb,_ca])
                    else:
                        BGL.lotext.render_text_pixels(nstr, cx-1,103,[x,x,x] )

                    #x = 1.0
                    #nstr = "{0} purity".format(self.total_points)
                    #BGL.lotext.render_text_pixels(nstr, cx,3,[0.0,0.0,0.0] )
                    #BGL.lotext.render_text_pixels(nstr, cx-1,2,[x,x,x] )

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
                
                for idx, message in enumerate(self.dm_messages):
                    message.render(idx, len(self.dm_messages))

        with BGL.blendmode.alpha_over:
            self.hud_buffer.render_processed( BGL.assets.get("beagle-2d/shader/passthru") )
            self.floor.render_objects("hud", True)


            self.heartcard.render()
            if(Abilities.Telekine):
                self.telekinecard.render()
                TelekineCooldown.render()

            if(Abilities.Sword):
                SwordCooldown.render()

        #for x in reversed(range(0,self.max_invslots)):
        #    if x is not self.sel_invslot:
        #        PlayerInvSlot.render(x, self.inventory[x], False, x == self.active_invslot)
        #PlayerInvSlot.render(self.sel_invslot, self.inventory[self.sel_invslot], True, self.sel_invslot == self.active_invslot)

        

        #self.potioncard.render()
        #self.potioncountview.render()

        #self.wandcard.render()


        
        with BGL.blendmode.alpha_over:
            self.swordcard.render()
            if(self.terminal_size>0):
                if self.get_camera().cinema_target is None:
                    TerminalRenderer.render(self.terminal_size, self.cardtick,self.active_terminal)

            self.time_buffer.render_processed( BGL.assets.get("beagle-2d/shader/passthru") )
            if(render_titlecard):
                self.title_card.render()



    def customize(self):

        #self.tooltip = "I'm the PLAYER!"
        self.health_count = 2
        self.dch_cooldown = 0
        self.active_invslot = None
        self.sel_invslot = 0
        self.max_invslots = 5

        self.active_terminal = None
        self.terminal_size = 0.0

        self.telekineFlash = 0.0
        self.potionFlash = 0.0

        self.inventory = [None] * self.max_invslots
        self.inventory[0] = "hp_vial"
        self.inventory[1] = "hp_vial"
        self.heartcard = HeartCard(self)
        self.swordcard = SwordCard(self)
        self.wandcard = WandCard(self)
        self.telekinecard = TelekineCard(self)
        self.potioncard = PotionCard(self)
        self.potioncountview = PotionCountView(self)
        #self.hp = 100
        self.dash_amt = 1.0
        self.sword = Sword(player=self)
        self.pumped_dashcombo = False
        self.can_backstep = True
        self.backstep_cooldown = -5
        self.backstepping = False
        self.cardtick = 0.0
        self.attack_object = None
        self.fire_timer = 0
        self.running = False

        self.hittable_hilight = []
        self.hittable_hint_real = 0.0
        self.hittable_hint_impulse = 0.0

        self.snap_animation_buffer = 0
        self.display_p = [0.0,0.0]

        self.run_stamina = 100.0
        self.stamina_recharge_buffer = 0.0
        self.slash = SlashEffect()
    
    def link_floor(self):
        self.violentally_executed_self = False
        self.floor.create_object( self.sword )
        self.floor.create_object( self.slash )

        self.total_kills = 0
        self.beat_level = False
        self.total_slashes = 0

        if "time_limit" in self.floor.__dict__:
            self.life_timer = self.floor.time_limit


    def get_shader_params(self):
        base_params = Player.get_shader_params(self)
        if self.hp > 0:
            base_params["rotation_local"] = 0.0
        if(self.snap_animation_buffer>0):
            #print(base_params)
            #print(self.display_p,self.p)
            base_params["texBuffer"] = KPlayer.BirdmanTextures[ int(KPlayer.BirdmanTick/5)%3 ]
            base_params["translation_world"] = self.get_camera().translate_position( self.display_p )
        if(self.shield_frames>0):
            base_params["texBuffer"] = KPlayer.BirdmanTextures[ int(KPlayer.BirdmanTick/5)%3 ]

        #if self.state == KPlayer.STATE_STUNNED:
        #    base_params["rotation_local"] = sin(self.cardtick)*0.2


        return base_params

    def get_guppy_batch(self):
        return [ self.get_shader_params() ]
        batch = [ Object.get_shader_params(self), self.get_shader_params() ]
        r = self.physics["radius"]
        #batch[0]["scale_local"] = [ r*2,r*2 ]
        #batch[0]["texBuffer"]=BGL.assets.get("KT-forest/texture/alpha_shadow")
        batch[0]["scale_local"] = [ r,r ]
        batch[0]["texBuffer"]=BGL.assets.get("KT-forest/texture/registration2")
        batch[1]["translation_local"][1] -= 0.0
        return batch
    
    def determine_texture(self):
        md = (self.v[0]*self.v[0])+(self.v[1]*self.v[1])
        idx = (
            ((0-rad_2_index(self.rad,8))+5) % 8
        )*4
        offs = self.run_animation_subtick//4

        print(offs)

        if(md>15):
            return KPlayer.vl2d_walk[idx + offs]
        else:
            return KPlayer.vl2d_idle[idx + offs]


    def _determine_texture(self):

        #if self.title_card.displaying():
        #    return KPlayer.textures[21]

        modamt = 1
        if self.dash_flash:
            modamt = modamt*3

        if self.sword_swing <= 0:
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
        KSounds.play( choice([ KSounds.enemy_killed, KSounds.enemy_killed2 ]) )
        self.kill_success = True
        self.total_kills += 1
        pass

    def deal_with_buttons(self,pad):

        self.X_STATE[0] = self.X_STATE[1]
        self.X_STATE[1] = pad.button_down( BGL.gamepads.buttons.X )
    
        if self.X_STATE[1] is True and self.X_STATE[0] is False:
            self.X_PRESSED = True
        else:
            self.X_PRESSED = False

        self.Y_STATE[0] = self.Y_STATE[1]
        self.Y_STATE[1] = pad.button_down( BGL.gamepads.buttons.Y )
    
        if self.Y_STATE[1] is True and self.Y_STATE[0] is False:
            self.Y_PRESSED = True
        else:
            self.Y_PRESSED = False

        self.LEFT_STATE[0] = self.LEFT_STATE[1]
        self.LEFT_STATE[1] = pad.button_down( BGL.gamepads.buttons.DPAD_LEFT )
    
        if self.LEFT_STATE[1] is True and self.LEFT_STATE[0] is False:
            self.LEFT_PRESSED = True
        else:
            self.LEFT_PRESSED = False

        self.RIGHT_STATE[0] = self.RIGHT_STATE[1]
        self.RIGHT_STATE[1] = pad.button_down( BGL.gamepads.buttons.DPAD_RIGHT )
    
        if self.RIGHT_STATE[1] is True and self.RIGHT_STATE[0] is False:
            self.RIGHT_PRESSED = True
        else:
            self.RIGHT_PRESSED = False

        self.UP_STATE[0] = self.UP_STATE[1]
        self.UP_STATE[1] = pad.button_down( BGL.gamepads.buttons.DPAD_UP )
    
        if self.UP_STATE[1] is True and self.UP_STATE[0] is False:
            self.UP_PRESSED = True
        else:
            self.UP_PRESSED = False

        self.DOWN_STATE[0] = self.DOWN_STATE[1]
        self.DOWN_STATE[1] = pad.button_down( BGL.gamepads.buttons.DPAD_DOWN )
    
        if self.DOWN_STATE[1] is True and self.DOWN_STATE[0] is False:
            self.DOWN_PRESSED = True
        else:
            self.DOWN_PRESSED = False

        self.A_STATE[0] = self.A_STATE[1]
        self.A_STATE[1] = pad.button_down( BGL.gamepads.buttons.A )
    
        if self.A_STATE[1] is True and self.A_STATE[0] is False:
            self.A_PRESSED = True
        else:
            self.A_PRESSED = False

        self.B_STATE[0] = self.B_STATE[1]
        self.B_STATE[1] = pad.button_down( BGL.gamepads.buttons.B )
    
        if self.B_STATE[1] is True and self.B_STATE[0] is False:
            self.B_PRESSED = True
        else:
            self.B_PRESSED = False

        if self.X_STATE[1] is False:
            self.snap_attack_frozen = False


        if self.Y_PRESSED:
            #if( self.health_count>0):
            #    self.consume_hp()

            if(self.sel_invslot == self.active_invslot):
                self.consume_inventory()
                self.active_invslot = None
            else:
                if(self.inventory[self.sel_invslot] is None) and (self.active_invslot is not None):
                    self.inventory[self.sel_invslot] = self.inventory[self.active_invslot]
                    self.inventory[self.active_invslot] = None
                    self.active_invslot = None
                else:
                    self.active_invslot = self.sel_invslot


    def route_terminal_input(self):
        if self.active_terminal:
            t = self.active_terminal.get_ui()
            if(self.UP_PRESSED):
                t.key_up()
                return True
            if(self.DOWN_PRESSED):
                t.key_down()
                return True
            if(self.LEFT_PRESSED):
                t.key_left()
                return True
            if(self.RIGHT_PRESSED):
                t.key_right()
                return True
            if(self.A_PRESSED):
                t.key_select()
                return True
            if(self.B_PRESSED):
                t.key_back()
                return True
            return False
        return False

                
            
    def consume_inventory(self):
        pass

        inv = self.inventory[ self.sel_invslot]
        self.inventory[self.sel_invslot] = None
        if(inv is "hp_vial"):
            self.consume_hp()

    def handle_ability(self):
        if(uniform(0.0,1.0)>0.8):
            self.floor.create_object( HealthBubble( p = [ self.p[0], self.p[1]]))
        self.v[0] *= 0.8
        self.v[1] *= 0.8
        self.floor.add_fog(self, 2.0)
        pass

    def trigger_title(self, title):
        self.title_card.reset(title)
        
    def tick(self):
        Cooldown.tick(self)
        self.size = [ 6.7,6.7 ]
        if(self.snap_animation_buffer>0):
            self.size = [ 2.2,2.2 ]

        self.run_animation_subtick = self.run_animation_subtick + 1

        if(self.run_animation_subtick==16):
            self.run_animation_subtick = 0
            self.run_animation_alt = 0


        if not self.beat_level and self.floor.genocide_enabled: #set in game
            if not self.suspend_time_penalty:
                self.life_timer -= 1
            else:
                self.suspend_time_penalty = False

            if(self.life_timer<0):
                self.hp = -1

        self.disp_life_timer = floor(self.life_timer/60)
        if(self.disp_life_timer<0):
            self.disp_life_timer = "!TIMES UP!"
            if not self.violentally_executed_self:

                if choice([True,False,False]):
                    KSounds.play( KSounds.basic_hit )
                    KSounds.play( KSounds.player_hurt )
                    for x in range(0,2):
                        self.floor.create_object(SplatterParticle( p = [self.floor.player.p[0], self.floor.player.p[1]], rad = uniform(-3.14,3.14)))
                    if self.life_timer < - 90:
                        self.violentally_executed_self = True

        self.title_card.tick()

        if(self.title_card.displaying()):
            self.texture = self.determine_texture()
            self.physics_suspended = True
            self.vx = 0
            self.vy = 0
            self.v = [0.0,0.0]
            if not self.in_editor:
                return True

        self.telekineFlash *= 0.95
        self.potionFlash *= 0.95


        teleportRecharge = 0.09
        if(self.teleportAmt < 100.0):
            self.teleportAmt += teleportRecharge

        if self.floor.camera.cinema_target:
            self.physics_suspended = True
            self.vx = 0
            self.vy = 0
            self.v = [0.0,0.0]
            return True
        self.physics_suspended = False

        if(self.flash_color[3]>0.1):
            self.flash_color[3] *= 0.95
        else:
            self.flash_color[3] *= 0.0

        if(self.active_terminal):
            if( self.terminal_size<1.0):
                self.terminal_size = (self.terminal_size*0.9) + 0.1
                if self.terminal_size > 0.99:
                    self.terminal_size = 1.0
        else:
            if(self.terminal_size>0):
                self.terminal_size = (self.terminal_size*0.78)
                if(self.terminal_size<0.01):
                    self.terminal_size = 0.0

        self.sword_swing -= 1
        if(self.run_stamina<0):
            self.run_stamina = 0

        if self.get_camera().cinema_target is not None:
            return

        if(self.ability_timeout>0):
            self.ability_timeout -= 1
            self.handle_ability()
            return True

        self.hittable_hint_real = (self.hittable_hint_real*0.99)+ (self.hittable_hint_impulse*0.01)
        self.hittable_hint_impulse *= 0.98
        if(self.LEFT_PRESSED):
            self.sel_invslot -= 1
            if(self.sel_invslot<0):
                self.sel_invslot = self.max_invslots -1
        if(self.RIGHT_PRESSED):
            self.sel_invslot += 1
            if(self.sel_invslot == self.max_invslots):
                self.sel_invslot = 0
        PlayerInvSlot.tick()

        self.dm_msg_cooldown += 1
        if self.dm_msg_cooldown > 300:
            self.deq_dm_message()
            self.dm_msg_cooldown = 0
            

        #player tick
        if self.got_time > 0:
            self.got_time -= 1
        self.subtick = (self.subtick + 1) % 60

        #if(self.run_stamina<=1.0):
        #    self.add_dm_message("You over exerted yourself")

        self.invuln_frames -= 1
        if(self.shield_frames>0):
            self.shield_frames -= 1
        KPlayer.BirdmanTick = KPlayer.BirdmanTick+1

        self.snap_animation_buffer -= 1
        if(self.snap_animation_buffer>0):
            self.display_p[0] = (self.display_p[0]*0.87) + (self.p[0]*0.13)
            self.display_p[1] = (self.display_p[1]*0.87) + (self.p[1]*0.13)

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
        self.telekinecard.tick()
        self.potioncard.tick()



        self.pumped_dashcombo = False
        if(self.hp < 0 ):
            #self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
            #self.light_color = [ 1.0,0.0,0.0,1.0]
            #self.light_radius = 100
            self.texture = BGL.assets.get('KT-player/texture/skeleton')
            self.size = [2.0,2.0]
            self.rad = atan2(self.p[0]-self.snapshot['p'][0],self.p[1]-self.snapshot['p'][1])
            return True
        else:
            pass
            #self.light_color = [ 1.0,0.8,0.8,1.0 ]
            #self.light_radius = 15
        pad = self.controllers.get_virtualized_pad( self.num )
        self.deal_with_buttons(pad)
        used_term = self.route_terminal_input()
        if used_term:
            print("USED TERMINAL")
            self.A_PRESSED = False
            self.B_PRESSED = False
            self.UP_PRESSED = False
            self.DOWN_PRESSED = False
            self.LEFT_PRESSED = False
            self.RIGHT_PRESSED = False
        if self.A_PRESSED:
            if Abilities.Sword:
                if self.slash.slash():
                    self.run_animation_subtick = 0
                    self.run_animation_alt = 1
            #self.add_dm_message("You swung your sword")
            #print("a pressed")
            #self.state = KPlayer.STATE_FIRING


        self.dch_cooldown -= 1
        if self.snap_cooldown < 0:
        #if (self.X_PRESSED and self.link_count>0) or ( (self.sword.state == Sword.STATE_CHARGING) and (self.sword.stimer == 10)):
            if (self.X_PRESSED) or ( (self.sword.state == Sword.STATE_CHARGING) and (self.sword.stimer == 10)) or (self.sword.state == Sword.STATE_DISCHARGING and self.dch_cooldown == 0):
                self.dch_cooldown = 17
                self.attempt_snap_attack()
                self.snap_cooldown = 4

        
        if(abs(pad.left_stick[0])>0.003) or (abs(pad.left_stick[1])>0.003):
            self.walk_tick = self.walk_tick+1
            if(self.walk_tick%100==1):
                KSounds.play(choice([KSounds.walk1,KSounds.walk2]))
            if(self.walk_tick>400):
                self.walk_tick = 0
        else:
            self.walk_tick = 0
 
        if(self.state == KPlayer.STATE_STUNNED ):
            self.v[0] = self.v[0] * 0.4
            self.v[1] = self.v[1] * 0.4

            #if(self.attack_object):
            #    self.v[0] = self.v[0] + (self.attack_object.v[0]*4)
            #    self.v[1] = self.v[1] + (self.attack_object.v[1]*4)

            if self.stimer > 15:
                self.attack_object = None
                self.set_state( KPlayer.STATE_DEFAULT )

        if(self.state == KPlayer.STATE_DODGING ):
            self.invisible_frames = 19 #also makes invuln
            for x in range(0,5):
                spltr = Bird( p = [self.p[0]+uniform(0.0,self.size[0]), self.p[1]+uniform(-4.0,4.0)])
                spltr.color = [0.0,0.0,0.0,1.0]
                spltr.light_color = [ 0.0,1.0,0.0,1.0]
                spltr.size[0]*=uniform(1.0,1.5)
                self.floor.create_object(spltr)

            #self.visible = False
            #self.invuln_frames = 1
            self.v[0] += self.dv[0]*2.8
            self.v[1] += self.dv[1]*2.8
            
            self.dv[0]*=0.6
            self.dv[1]*=0.6

            if(self.sword.state is not Sword.STATE_IDLE):
                self.set_state(KPlayer.STATE_DEFAULT)
            if(self.stimer > 6 ):
                self.visible = True
                self.set_state(KPlayer.STATE_DEFAULT)

        if(self.state == KPlayer.STATE_FIRING):
            self.fire_timer = self.fire_timer + 1
            self.v[0] = self.v[0] * 0.4
            self.v[1] = self.v[1] * 0.4
            delta = [ pad.left_stick[0] , pad.left_stick[1]  ]
            self.v[0] = self.v[0] + (delta[0]*0.2)
            self.v[1] = self.v[1] + (delta[1]*0.2)
            self.rad = atan2( self.v[1], self.v[0] )


            if(self.fire_timer>8):
                self.lazer_beam.visible = True
                self.lazer_beam.size[1] *= 1.15

                #if(self.fire_timer==20):
                #    self.attempt_snap_attack(False)
            if(self.fire_timer>40):
                self.lazer_beam.size[1] = 0.1
                self.lazer_beam.visible = False
                self.fire_timer = 0
                self.state = KPlayer.STATE_DEFAULT

        if(self.state == KPlayer.STATE_DEFAULT ):
            if not pad.button_down( BGL.gamepads.buttons.B ):
                self.can_backstep = True

            if(Abilities.Dash and pad.button_down( BGL.gamepads.buttons.B ) and self.can_backstep and self.sword.state == Sword.STATE_IDLE):

                if(self.stimer > 30 ):
                    if(self.run_stamina>5):
                        self.run_stamina -= 5
                        delta = [ pad.left_stick[0] , pad.left_stick[1]  ]
                        self.dv = [ delta[0] * self.speed, delta[1] * self.speed ]
                        self.can_backstep = False
                        self.set_state(KPlayer.STATE_DODGING)
                        #self.attempt_snap_attack()
                        self.combo_reset_cooldown = 60*KPlayer.ComboSecs
                        if(self.link_count==0):
                            self.link_count = 1

                        self.flash_color = [1.0,1.0,1.0,1.0]
                        KSounds.play( KSounds.dash )
                    
            calc_speed = self.speed

            
            if(self.run_stamina<1.0):
                self.flash_color = [ 1.0,0.6,0.6,1.0 ]
                calc_speed *= 0.2
            if(pad.button_down( BGL.gamepads.buttons.RIGHT_BUMPER) and Abilities.Dash):
                if(self.run_stamina>0.0):
                    self.running = True
                    self.stamina_recharge_buffer = 10.0
                    self.run_stamina -= 0.45
                    rs1 = self.run_stamina/75.0
                    rs2 = rs1*rs1;
                    mod1 = 0.8 * rs1 
                    mod2 = 1.1 * rs2
                    calc_speed *= 1.0+(mod1+mod2)
                    if(self.slash.visible):
                        mod1*=1.5
            else:
                self.stamina_recharge_buffer -= 0.2
                if(self.stamina_recharge_buffer<0.0):
                    if(self.run_stamina<100.0):
                        self.run_stamina += 1.0

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

            #if(self.state == KPlayer.STATE_FIRING):
            #    self.v[0] = self.v[0] * 0.01
            #    self.v[1] = self.v[1] * 0.01

            calc_speed = self.filtered_speed
            Object.tick(self)
            pad = self.controllers.get_virtualized_pad( self.num )

                #delta = [0.0,0.0]
                #self.v[0] = self.v[0]*0.8+delta[0]*0.2
                #self.v[1] = self.v[1]*0.8+delta[1]*0.2
            delta = [ pad.left_stick[0] * calc_speed, pad.left_stick[1] * calc_speed ]
            self.v[0] = self.v[0]*0.8+delta[0]*0.2
            self.v[1] = self.v[1]*0.8+delta[1]*0.2

            self.rad = atan2( self.v[1], self.v[0] )
            self.texture = self.determine_texture()

            if(self.snap_cooldown>0):
                self.v[0] = 0
                self.v[1] = 0
            

            if(self.snap_attack_frozen):
                self.v[0] = 0
                self.v[1] = 0 

            if(self.attack_physics_timer>0 and self.attack_object):#the and here is a hack around a bug

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
        
            if(self.slash.visible):
                self.v[0] *= 1.05
                self.v[1] *= 1.05


            if(abs(self.v[0]) + abs(self.v[1])>0.5):
                if uniform(0.0,1.0)>0.98:
                    self.floor.create_object(Dust( p=[ self.p[0], self.p[1]+0.8]))

            Object.tick(self)
            if self.invisible_frames > 0:
                self.invisible_frames -= 1
                self.invuln_frames = 2
                self.visible = False
            else:
                self.visible = True

