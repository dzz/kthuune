from Newfoundland.Object import Object
from Beagle import API as BGL

class Trigger(Object):
    textures = BGL.assets.get('KT-forest/animation/decorators')

    def parse(od,df):

        x1 = float(od["x"])
        y1 = float(od["y"])

        x2 = float(od["w"])
        y2 = float(od["h"])

        cx = (x1+x2) / 2.0
        cy = (y1+y2) / 2.0
      
        w = (x2-x1)*0.5
        h = (y2-y1)*0.5

        group = od["meta"]["group"]
        return Trigger(
            group = group,
            p=[cx,cy],
            size=[w,h],
            scale_uv=[1.0,1.0],
            tick_type = Object.TickTypes.PURGING,
            visible = False,
            buftarget = "floor",
            light_type = Object.LightTypes.NONE
            )

    def tick(self):
        print("TRIGGER TICK")
        if(self.floor.player.p[0] > self.p[0]-self.size[0]):
            if(self.floor.player.p[0] < self.p[0]+self.size[0]):
                if(self.floor.player.p[1] > self.p[1]-self.size[1]):
                    if(self.floor.player.p[1] < self.p[1]+self.size[1]):
                        if self.group in self.floor.trigger_callbacks:
                            self.floor.trigger_callbacks[self.group](self)
                        return False
        return True

