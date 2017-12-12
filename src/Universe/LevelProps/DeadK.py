from Newfoundland.Object import Object
from Beagle import API as BGL

class DeadK(Object):
    def parse(od,df):
        DeadK.instance = DeadK(p=[od["x"],od["y"]])
        return DeadK.instance

    def customize(self):
        self.buftarget = "popup"
        self.size = [ 11.0,11.0 ]
        self.light_color = [ 1.0,0.6,0.6,1.0 ]
        self.light_radius = 20
        self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
        self.visible = True
        self.texture = BGL.assets.get("KT-forest/texture/deadk1")
        self.tick_type = Object.TickTypes.STATIC
        self.z_index = 1
        #self.physics = { "radius" : 1.0, "mass"   : 900, "friction" : 0.3 }

    def get_shader_params(self):
        sp = Object.get_shader_params(self)
        return sp
