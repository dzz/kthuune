from Newfoundland.Object import Object
from Beagle import API as BGL

class BlindArcade(Object):
    texture = BGL.assets.get('KT-forest/texture/blindarcade')

    def parse(od,df):

        x1 = float(od["x"])
        y1 = float(od["y"])

        x2 = float(od["w"])
        y2 = float(od["h"])

        cx = (x1+x2) / 2.0
        cy = (y1+y2) / 2.0
      
        w = (x2-x1)*0.5
        h = (y2-y1)*0.5

        return BlindArcade(
            p=[cx,cy],
            size=[w,h],
            scale_uv=[1.0*(w*0.5),1.0],
            tick_type = Object.TickTypes.STATIC,
            visible = True,
            buftarget = "floor",
            texture = BlindArcade.texture
            )
