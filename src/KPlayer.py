from Beagle import API as BGL
from Newfoundland.Object import Object
from Newfoundland.Player import Player
from random import uniform
from math import floor,pi

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
            "z_index" : 1
        }
        overrides.update(kwargs)
        Player.__init__(self, **overrides)
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

    def get_shader_params(self):
        base_params = Player.get_shader_params(self)
        base_params["rotation_local"] = 0.0
        return base_params
        
    def determine_texture(self):
        tex = KPlayer.textures[4]

        yidx = 0
        if(self.rad > 0):
            yidx = 3



        print(self.rad)
        print(rad_2_index(self.rad, 8))
        

        xidx = int((abs(self.rad)/3.14)*3)

        #idx = (yidx+(2-xidx))*3

        idx = rad_2_index(self.rad,8)*3

        widx = (self.walk_tick//40) % 4
        woffs = [ 0,1,0,2 ]
        tex = KPlayer.textures[idx+woffs[widx]]
        return tex
 
    def tick(self):

        pad = self.controllers.get_virtualized_pad( self.num )

        if(abs(pad.left_stick[0])>0.003) or (abs(pad.left_stick[1])>0.003):
            self.walk_tick = self.walk_tick+1
            if(self.walk_tick>400):
                self.walk_tick = 0
        else:
            self.walk_tick = 0
 
        Player.tick(self)
        impulse = uniform(5.0,35.0)
        self.light_radius = (self.light_radius*0.96) + (impulse*0.04)
        self.texture = self.determine_texture()
