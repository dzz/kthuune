from Beagle import API as BGL
from Newfoundland.Object import Object
from Newfoundland.Player import Player
from random import uniform
from math import floor,pi,atan2

def rad_2_index(rad, segments):
    segment_amt = ((2*pi)/segments)
    rad -= (segment_amt*0.5) # center
    rad += pi
    segment = floor((rad/segment_amt)%segments)
    return int(segment)

class KPlayer(Player):

 
    def __init__(self, **kwargs):
        overrides =  {
            "light_type" : Object.LightTypes.DYNAMIC_SHADOWCASTER,
            "light_radius" : 15.0,
            "light_color" : [ 0.65,0.45,0.3,1.0],
            "walk_tick" : 0,
            "z_index" : 1,
            "sword_swing" : 0,
            "sword_swing_cooldown" : 60,
            "sword_released" : True,
            "filtered_speed" : 0.0,
            "buftarget" : "popup"
        }
        overrides.update(kwargs)
        Player.__init__(self, **overrides)
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

    def customize(self):
        self.hp = 100

    def get_shader_params(self):
        base_params = Player.get_shader_params(self)
        if self.hp > 0:
            base_params["rotation_local"] = 0.0
        return base_params
        
    def determine_texture(self):

        if self.sword_swing == 0:
            tex = KPlayer.textures[4]

            yidx = 0
            if(self.rad > 0):
                yidx = 3
            idx = rad_2_index(self.rad,8)*3
            widx = (self.walk_tick//40) % 4
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
 
    def tick(self):

        if(self.hp < 0 ):
            self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
            self.light_color = [ 1.0,1.0,0.0,1.0]
            self.light_radius = 100
            self.texture = BGL.assets.get('KT-player/texture/skeleton')
            self.size = [1.0,1.0]
            self.rad = atan2(self.p[0]-self.snapshot['p'][0],self.p[1]-self.snapshot['p'][1])
            print (self.rad)
            return True
        pad = self.controllers.get_virtualized_pad( self.num )

        if(self.sword_swing>0):
            self.sword_swing = self.sword_swing - 1
        else:

            if self.sword_released:
                if pad.button_down( BGL.gamepads.buttons.RIGHT_BUMPER ):
                    self.sword_swing = self.sword_swing_cooldown
                    self.sword_released = False
            else:
                if not pad.button_down(BGL.gamepads.buttons.RIGHT_BUMPER):
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

        delta = [(pad.left_stick[0])*calc_speed,(pad.left_stick[1])*calc_speed]

        self.v[0] = self.v[0]*0.8+delta[0]*0.2
        self.v[1] = self.v[1]*0.8+delta[1]*0.2

        self.dir = ( pad.right_stick[0], pad.right_stick[1] )
        self.rad = atan2( self.dir[1], self.dir[0] )

        ##########
        impulse = uniform(5.0,35.0)
        self.light_radius = (self.light_radius*0.96) + (impulse*0.04)
        self.texture = self.determine_texture()
