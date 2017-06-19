from Newfoundland.Object import Object
from Newfoundland.Player import Player
from random import uniform

class KPlayer(Player):
    def __init__(self, **kwargs):
        overrides =  {
            "light_type" : Object.LightTypes.DYNAMIC_SHADOWCASTER,
            "light_radius" : 15.0,
            "light_color" : [ 0.65,0.45,0.3,1.0]
        }
        overrides.update(kwargs)
        Player.__init__(self, **overrides)

    def tick(self):
        Player.tick(self)
        impulse = uniform(5.0,15.0)

        self.light_radius = (self.light_radius*0.96) + (impulse*0.04)
