from Beagle import API as BGL
from Newfoundland.Object import Object
from Newfoundland.Player import Player
from random import uniform
from math import floor,pi,atan2,sin, hypot

def rad_2_index(rad, segments):
    segment_amt = ((2*pi)/segments)
    rad -= (segment_amt*0.5) # center
    rad += pi
    segment = floor((rad/segment_amt)%segments)
    return int(segment)

class Sword(Object):
    def __init__(self,**kwargs):
        Object.__init__(self,**kwargs)

    def customize(self):
        self.tick_type = Object.TickTypes.TICK_FOREVER
        self.texture = BGL.assets.get('KT-player/texture/sword')
        self.buftarget = "popup"
        self.z_index = 2
        self.bob_index = 0.0
        self.collected = True

    def tick(self):

        if not self.collected:
            if hypot( self.p[0]-self.player.p[0],self.p[1]-self.player.p[1]) < 1.5:
                self.collected = True
            return

        self.bob_index = self.bob_index + 0.04
        self.p[0] = self.player.p[0]
        self.p[1] = self.player.p[1]

        if(self.player.sword_swing>0.0):

            self.size = [1.1,1.1]
            ramt = self.player.sword_swing / self.player.sword_swing_cooldown

            ramt = ramt*ramt
            ramt = 1.0 - ramt
            self.rad = self.player.rad-(2.8)+(1.8*-4*ramt)

            self.size[0] = self.size[0] + (ramt*0.3)
        else:
            self.size = [1.0,1.0]
            bob = sin(self.bob_index)
            if(self.player.rad > 0.0): self.rad = (-2.9-3.14) + (self.player.rad*0.1*bob)
            if(self.player.rad < 0.0): self.rad = (2.7) - (self.player.rad*0.1*bob)

        if(self.player.rad > 0.0): self.z_index = 2
        if(self.player.rad < 0.0): self.z_index = 0

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
            "sword_swing_cooldown" : 25,
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

    def customize(self):
        self.hp = 100
        self.dash_amt = 1.0
        self.sword = Sword(player=self)
        self.pumped_dashcombo = False
    
    def link_floor(self):
        self.floor.create_object( self.sword )

    def get_shader_params(self):
        base_params = Player.get_shader_params(self)
        if self.hp > 0:
            base_params["rotation_local"] = 0.0
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
        self.attacked = True
        self.hp = self.hp - damage

    def is_dashing(self):
        return self.dash_combo

    def next_dashcombo(self):
        self.dash_combo = True
        self.dash_amt = self.dash_amt * 1.1
        self.pumped_dashcombo = True

    def pump_dashcombo(self):
        if(self.dash_combo):
            if not self.pumped_dashcombo:
                self.dash_amt = self.dash_amt*1.09
                self.pumped_dashcombo = True
                self.dash_combo = True

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
            else:
                if not pad.button_down(BGL.gamepads.buttons.A):
                    self.sword_released = True
                    

        if(abs(pad.left_stick[0])>0.003) or (abs(pad.left_stick[1])>0.003):
            self.walk_tick = self.walk_tick+1
            if(self.walk_tick>400):
                self.walk_tick = 0
        else:
            self.walk_tick = 0
 
        ###Player.tick(self)

        calc_speed = self.speed

        if(self.sword_swing>0):
            calc_speed = self.speed * 0.28

        if(self.aiming_beam.aiming):
            calc_speed = calc_speed * 0.5


        self.filtered_speed = (self.filtered_speed*0.8) + (calc_speed*0.2)
        calc_speed = self.filtered_speed

        Object.tick(self)

        pad = self.controllers.get_virtualized_pad( self.num )

        self.dash_flash = False

        dashcheck = 0.3
        if(pad.button_down(BGL.gamepads.buttons.A)):
            dashcheck = 0.18

        if(self.dash_amt > dashcheck) and self.is_dashing():
            calc_speed = calc_speed + (11.0*self.dash_amt)
            self.dash_amt = self.dash_amt * 0.954
            self.dash_flash = True
        else:
            self.dash_combo = False
            if not pad.button_down(BGL.gamepads.buttons.Y):
                if(self.dash_amt<1.0):
                    self.dash_amt = self.dash_amt * 1.3

        

        delta = [(pad.left_stick[0])*calc_speed,(pad.left_stick[1])*calc_speed]




        self.v[0] = self.v[0]*0.8+delta[0]*0.2
        self.v[1] = self.v[1]*0.8+delta[1]*0.2

        #ndir = ( pad.right_stick[0], pad.right_stick[1] )
        #self.dir = [ (self.dir[0]*0.9) +(ndir[0]*0.1), (self.dir[1]*0.9) + (ndir[1]*0.1) ]

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
    

        ##########
