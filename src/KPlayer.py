from Beagle import API as BGL
from Newfoundland.Object import Object
from Newfoundland.Player import Player
from random import uniform,choice
from math import floor,pi,atan2,sin, hypot

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

    max_charge = 40
    max_pending = 60
    max_discharge = 10

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



    def tick(self):

        pad = self.player.controllers.get_virtualized_pad( self.player.num )
        btns = BGL.gamepads.buttons

        self.stimer = self.stimer + 1
        if self.state == Sword.STATE_IDLE:
            self.stimer = 0
            if pad.button_down( btns.A ):
                self.state = Sword.STATE_CHARGING
                self.stimer = 0

        if self.state == Sword.STATE_CHARGING:
            self.discharge_mod = self.discharge_mod * 1.02
            if not pad.button_down( btns.A ):
                self.state = Sword.STATE_DISCHARGING
                self.stimer = 0
            if self.stimer >= Sword.max_charge:
                self.state = Sword.STATE_ATTACK_PENDING
                self.stimer = 0

        if self.state == Sword.STATE_ATTACK_PENDING:
            if self.stimer >= Sword.max_pending or (not pad.button_down(btns.A)):
                self.stimer = 0
                self.state = Sword.STATE_DISCHARGING

        if self.state == Sword.STATE_DISCHARGING:
            if self.stimer >= (Sword.max_discharge * self.discharge_mod):
                self.stimer = 0
                self.state = Sword.STATE_AWAITING_RELEASE

        if self.state == Sword.STATE_AWAITING_RELEASE:
            self.discharge_mod = 1.0
            if not pad.button_down( btns.A):
                self.state = Sword.STATE_IDLE
            
        print(self.state, self.stimer)

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
    def __init__(self, **kwargs):
        overrides =  {
            "light_type" : Object.LightTypes.DYNAMIC_SHADOWCASTER,
            "light_radius" : 15.0,
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
        }
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
        self.can_combo = False
        self.kill_success = False
        self.target_consumed = False
        self.target_cooldown = 0.0


    def render_hud(self):
        with BGL.context.render_target( self.hud_buffer ):
            BGL.context.clear(0.0,0.0,0.0,0.0)
            with BGL.blendmode.alpha_over:
                BGL.lotext.render_text_pixels("HP:{0}".format(self.hp-1), 130,220,[1.0,0.0,0.0] )
                if(self.combo_count>1):
                    offsx = choice(range(-3,3))
                    offsy = choice(range(-2,2))
                    BGL.lotext.render_text_pixels("COMBO:{0}".format(self.combo_count-1), 130+offsx,90+offsy, [1.0,uniform(0.0,1.0),1.0] )

        with BGL.blendmode.alpha_over:
            self.hud_buffer.render_processed( BGL.assets.get("beagle-2d/shader/passthru") )

    def customize(self):
        self.hp = 100
        self.dash_amt = 1.0
        self.sword = Sword(player=self)
        self.pumped_dashcombo = False
        self.can_backstep = True
        self.backstep_cooldown = -5
        self.backstepping = False
    
    def link_floor(self):
        self.floor.create_object( self.sword )

    def get_shader_params(self):
        base_params = Player.get_shader_params(self)
        if self.hp > 0:
            base_params["rotation_local"] = 0.0
            if(self.combo_count>3):
                sl = base_params['scale_local']
                base_params['scale_local'] = [ sl[0] + uniform(0.1,0.3), sl[1] + uniform(0.1,0.3) ]
                base_params['scale_local'] = sl
                base_params['filter_color'] = [ uniform(0.5,1.0),uniform(0.5,1.0),uniform(0.5,1.0),1.0]

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
        if(self.combo_count <= 2):
            if(self.sword_swing<5):
                self.attacked = True
                self.hp = self.hp - damage

    def is_dashing(self):
        return self.dash_combo

    def notify_succesful_attack(self):
        pass

    def next_dashcombo(self):
        self.dash_combo = True

        if(self.combo_count<20):
            self.dash_amt = self.dash_amt * 1.2
        self.pumped_dashcombo = True

        if(self.can_combo):
            self.combo_count = self.combo_count + 1
            self.can_combo = False

    def pump_dashcombo(self):
        if(self.dash_combo):
            if(self.can_combo):
                self.combo_count = self.combo_count + 1
                self.can_combo = False
            if not self.pumped_dashcombo:
                if(self.combo_count<20):
                    self.dash_amt = self.dash_amt * 1.2
                else:
                    self.dash_amt = self.dash_amt*1.05
                self.pumped_dashcombo = True
                self.dash_combo = True


    def notify_enemy_killed(self):
        self.kill_success = True
        pass

    def tick(self):

        self.pumped_dashcombo = False
        if(self.hp < 0 ):
            self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
            self.light_color = [ 1.0,0.0,0.0,1.0]
            self.light_radius = 100
            self.texture = BGL.assets.get('KT-player/texture/skeleton')
            self.size = [1.0,1.0]
            self.rad = atan2(self.p[0]-self.snapshot['p'][0],self.p[1]-self.snapshot['p'][1])
            print (self.rad)
            return True
        pad = self.controllers.get_virtualized_pad( self.num )

        

        self.backstep_cooldown = self.backstep_cooldown - 1
        if(pad.button_down( BGL.gamepads.buttons.B)) and self.can_backstep:
            self.can_combo = True
            self.can_backstep = False
            self.backstepping = True
            self.backstep_cooldown = 40.0
            self.dash_amt = self.dash_amt*1.4

        if(self.backstepping):
            if(self.backstep_cooldown<0.0):
                self.backstepping = False 

        if( not self.backstepping and not pad.button_down( BGL.gamepads.buttons.B)):
            self.can_backstep = True


        if(self.sword_swing>0):
            self.sword_swing = self.sword_swing - 1
            self.light_color = [0.2,0.3,1.0,1.0]
            if uniform(0.0,1.0)<0.1:
                self.light_color = [0.0,0.0,0.0,1.0]
        else:
            self.light_color = self.base_light_color
            if self.sword_released:
                if pad.button_down( BGL.gamepads.buttons.A ):
                    self.sword_swing = self.sword_swing_cooldown
                    self.sword_released = False
                    self.can_combo = True
            else:
                if(self.sword_swing_cooldown>5.0):
                    if pad.button_down( BGL.gamepads.buttons.A ):
                        self.can_combo = False
                        self.dash_combo = False
                if not pad.button_down(BGL.gamepads.buttons.A):
                    self.sword_released = True
        
        ### new sword charge mode            


        ###

        if(abs(pad.left_stick[0])>0.003) or (abs(pad.left_stick[1])>0.003):
            self.walk_tick = self.walk_tick+1
            if(self.walk_tick>400):
                self.walk_tick = 0
        else:
            self.walk_tick = 0
 
        ###Player.tick(self)

        calc_speed = self.speed

        self.dash_flash = False
        if(self.sword.state == Sword.STATE_CHARGING):
            calc_speed = self.speed * 0.1

        if(self.sword.state == Sword.STATE_DISCHARGING):
            self.dash_flash = True
            calc_speed = self.speed * 9.0

        if(self.sword.state == Sword.STATE_ATTACK_PENDING):
            self.dash_flash = True
            calc_speed = self.speed * 0.001

        if(self.aiming_beam.aiming):
            calc_speed = calc_speed * 0.5


        self.filtered_speed = (self.filtered_speed*0.8) + (calc_speed*0.2)
        calc_speed = self.filtered_speed

        Object.tick(self)

        pad = self.controllers.get_virtualized_pad( self.num )

        #self.dash_flash = False

        #dashcheck = 0.3
        #if(pad.button_down(BGL.gamepads.buttons.A)):
        #    dashcheck = 0.18

        #if(self.dash_amt > dashcheck) and self.is_dashing():
        #    calc_speed = calc_speed + (11.0*self.dash_amt)

        #    self.dash_amt = self.dash_amt * 0.954
        #    self.dash_flash = True
        #else:
        #    self.dash_combo = False
        #    if(self.dash_amt<1.0):
        #        self.dash_amt = self.dash_amt * 1.3

        #calc_speed = min(calc_speed,12.0)
        #
        if(self.backstepping):
            calc_speed = calc_speed * - (1.2+(self.backstep_cooldown/40.0)*0.2)
        delta = [(pad.left_stick[0])*calc_speed,(pad.left_stick[1])*calc_speed]

        target = None

        ##### self.target_cooldown = self.target_cooldown - 1
        ##### if((not self.target_consumed) or self.target_cooldown >0.0) and (pad.button_down(BGL.gamepads.buttons.A)):

        #####     if(not self.target_consumed):
        #####         self.target_consumed = True
        #####         self.target_cooldown = 40.0
        #####     #self.dash_amt = self.dash_amt * 1.3
        #####     local_enemies = list(filter(lambda x: x.should_draw() and x.__class__.__name__ == 'Worm' and x.hp > 0.0, self.floor.objects))
        #####     local_enemies.sort(key = lambda x: hypot(self.p[0]-x.p[0],self.p[1]-x.p[1]))
        #####     if(len(local_enemies)>0):
        #####         target = local_enemies[0]

        ##### if not(pad.button_down(BGL.gamepads.buttons.A)):
        #####     self.target_consumed = False


        if not target:
            self.v[0] = self.v[0]*0.8+delta[0]*0.2
            self.v[1] = self.v[1]*0.8+delta[1]*0.2
        else:
            dx = target.p[0] - self.p[0]
            dy = target.p[1] - self.p[1]
            #self.v[0] = target.p[0] - self.p[0]
            #self.v[1] = target.p[1] - self.p[1]
            tscl = 15.0
            if(self.backstepping):
                tscl *= -1
            l = hypot(dx,dy)
            if(l<17):
                self.v[0] = (dx / l)*tscl
                self.v[1] = (dy / l)*tscl


        #ndir = ( pad.right_stick[0], pad.right_stick[1] )
        #self.dir = [ (self.dir[0]*0.9) +(ndir[0]*0.1), (self.dir[1]*0.9) + (ndir[1]*0.1) ]

        if(self.backstep_cooldown < -5.0 ):
            self.rad = atan2( self.v[1], self.v[0] )



        if(self.attacked):
            self.light_color = [ 1.0,0.0,0.0,1.0 ]
            self.light_radius = uniform(0.0,200.0)
            self.v[0] = self.v[0]*-10
            self.v[0] = self.v[1]*-10

            if (abs(self.v[0])<0.01) or (abs(self.v[1])<0.01):
                self.v[0] = uniform(-1.0,1.0)
                self.v[1] = uniform(-1.0,1.0)
            self.attacked = False
        else:
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

        if not self.dash_combo:
            self.combo_count = 0
        ##########
