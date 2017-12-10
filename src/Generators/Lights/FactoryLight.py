from Newfoundland.Object import Object
from Beagle import API as BGL
from random import uniform

class FactoryLight(Object):
    def customize(self):
        self.visible = False
        self.tick_type = Object.TickTypes.STATIC
        self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
        self.light_radius = 100
        self.p = [ self.factory_def['x'], self.factory_def['y'] ]
        if self.factory_def["meta"]["class"] == "red_test":
            self.light_color = [ 1.0, 0.2,0.2,1.0 ]
        if self.factory_def["meta"]["class"] == "blue_test":
            self.light_color = [ 0.2, 0.2,1.0,1.0 ]
        if self.factory_def["meta"]["class"] == "green":
            self.light_radius = 25.
            self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
            self.light_color = [ 0.5, 1.0,0.8,1.0 ]
        if self.factory_def["meta"]["class"] == "shiplight":
            self.light_radius = 45.
            self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
            self.light_color = [ 1.0, 1.0,1.0,1.0 ]
        if self.factory_def["meta"]["class"] == "shipfill":
            self.light_radius = 25.
            self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
            self.light_color = [ 0.5, 0.6,1.0,1.0 ]
        if self.factory_def["meta"]["class"] == "spacefill":
            self.light_radius = 45.
            self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
            self.light_color = [ 0.7, 0.9,1.0,1.0 ]
        if self.factory_def["meta"]["class"] == "green_afterbirth":
            self.light_radius = 25.
            self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
            self.light_color = [ 0.1, 0.8,0.3,1.0 ]
        if self.factory_def["meta"]["class"] == "shipfillred":
            self.light_radius = 35.
            self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
            self.light_color = [ 0.6, 0.3,0.2,1.0 ]
        if self.factory_def["meta"]["class"] == "iact":
            self.light_radius = 18.
            self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
            self.light_color = [ 0.3, 0.6,0.8,1.0 ]
        if self.factory_def["meta"]["class"] == "medium_oort_guider":
            self.light_radius = 15.
            self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
            self.light_color = [ 1.0, 0.5,1.0,0.7 ]
        if self.factory_def["meta"]["class"] == "large_oort_guider":
            self.light_radius = 30.
            self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
            self.light_color = [ 1.0, 1.0,1.0,0.7 ]
        if self.factory_def["meta"]["class"] == "oort_level_guider":
            self.light_radius = 90.
            self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
            self.light_color = [ 0.6, 1.0,0.0,0.5 ]
        if self.factory_def["meta"]["class"] == "shortwave":
            self.tick_type = Object.TickTypes.TICK_FOREVER
            self.animation_type = 0
            self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
            self.light_radius = uniform(10.0,40.0)
            self.light_color = [
                                uniform(0.2,0.6),
                                uniform(0.0,0.4),
                                uniform(0.5,1.0),
                                1.0 ]

    def tick(self):
        if(self.animation_type==0): #shortwave
            self.light_radius = (uniform(10.0,40.0)*0.1)+self.light_radius*0.9
            self.light_color = [
                                (uniform(0.2,0.6)*0.1) + self.light_color[0]*0.9,
                                (uniform(0.0,0.4)*0.1) + self.light_color[1]*0.9,
                                (uniform(0.5,1.0)*0.1) + self.light_color[2]*0.9,
                                1.0 ]
