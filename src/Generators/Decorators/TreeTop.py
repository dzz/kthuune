from Newfoundland.Object import Object
from Beagle import API as BGL
from math import sin,cos,pi
from random import uniform,choice
from ...GeneratorOptions import GeneratorOptions
from ..Configuration.vconf import vconf

class TreeTop(Object):
        def __init__(self,**kwargs):

            tex_options =  GeneratorOptions.TreeTopTextures

            overrides = {
                    "num" : 0,
                    "texture" : choice(tex_options),
                    'tick_type' : Object.TickTypes.TICK_FOREVER,
                    'size' : [ 5.0,5.0],
                    'rad' : uniform(-3.14,3.14),
                    'parallax' : 1.2,
                    'z_index' : 100,
                    'wind_speed' : uniform(0.1,0.3),
                    'wind_mod' : uniform(1.1,1.2),
                    'buftarget' : 'canopy'
                }


            overrides.update(kwargs)
            Object.__init__(self,**overrides)
            self.t = 0
            self.base_size = [ self.size[0], self.size[1] ]
            self.draw_color = [0.9,uniform(0.8,1.0),0.9,uniform(0.6,0.9)]
            self.last_a = self.draw_color[3]
            #if(self.texture == BGL.assets.get("KT-forest/texture/treetop2")):
            #    self.z_index = self.z_index + 1

        def tick(self):
            self.t = self.t + 0.01
            if(self.should_draw()):
                self.size[0] = self.base_size[0] * ( 4.0 + (1.5*(sin(self.t* self.wind_speed))))
                self.size[1] = self.base_size[1] * ( 4.0 + (1.5*(cos(self.t* self.wind_speed*self.wind_mod))))

            
            return True

        def should_draw(self):
            return True
            #p = self.get_shader_params()['translation_world']
            #visRad = vconf.visRad
            #if(p[0]<-visRad): return False
            #if(p[1]<-visRad): return False
            #if(p[0]>visRad): return False
            #if(p[1]>visRad): return False
            #return True

        def get_shader_params(self):
            params = Object.get_shader_params(self)
            tw = params["translation_world"]
            tw[0] = tw[0]*self.parallax
            tw[1] = tw[1]*self.parallax
            params["translation_world" ] = tw
            params["filter_color"] = list(self.draw_color)

            dx = self.p[0] - (self.floor.camera.p[0]+(self.floor.player.v[0]*3))
            dy = self.p[1] - (self.floor.camera.p[1]+(self.floor.player.v[1]*3))
            md = (dx*dx)+(dy*dy)
            impulse_a = self.draw_color[3]
            if(md < 250):
                impulse_a = 0.1

            self.last_a = (self.last_a * 0.98) + (impulse_a*0.02)
            params["filter_color"][3] = self.last_a
                
            return params
