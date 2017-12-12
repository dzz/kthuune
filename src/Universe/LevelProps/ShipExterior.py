from Newfoundland.Object import Object
from Beagle import API as BGL
from math import sin,cos

class ShipExterior(Object):
    texture = BGL.assets.get("KT-player/texture/ship_exterior")

    def parse(od,df):
        return ShipExterior( p=[ od['x'],od['y'] ] )

    def customize(self):
        self.texture = ShipExterior.texture
        self.visible = True
        self.tick_type = Object.TickTypes.TICK_FOREVER
        self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
        self.light_radius = 100
        self.light_color = [1.0,1.0,1.0,1.0]
        self.fridx = 0
        self.base_p = [ self.p[0], self.p[1] ]
        self.buftarget = "underfloor"
        self.size = [ 50.0,50.0 ]
        self.z_index = -1100
        self.parallax = 0.9

    def tick(self):
        self.fridx += 0.004
        self.p[1] = self.base_p[1] + (sin(self.fridx)*2)
        return True

    def get_shader_params(self):
        params = Object.get_shader_params(self)
        tw = params["translation_world"]
        tw[0] = tw[0]*self.parallax
        tw[1] = tw[1]*self.parallax
        params["translation_world" ] = tw
        return params
