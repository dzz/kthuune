from Newfoundland.Object import Object
from Beagle import API as BGL

class Decorator(Object):
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

        if "decorator_id" in od["meta"]:
            texture = Decorator.textures[od["meta"]["decorator_id"]]
        else:
            texture = Decorator.textures[0]
        if "self_lit" in od["meta"]:
            if od["meta"]["self_lit"]:
                light_type = Object.LightTypes.DYNAMIC_TEXTURE_OVERLAY
            else:
                light_type = Object.LightTypes.NONE

        return Decorator(
            p=[cx,cy],
            size=[w,h],
            scale_uv=[1.0,1.0],
            tick_type = Object.TickTypes.STATIC,
            visible = True,
            buftarget = "floor",
            texture = texture,
            light_type = light_type
            )
