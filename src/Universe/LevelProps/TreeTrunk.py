from Newfoundland.Object import Object
from Beagle import API as BGL
from random import choice

class TreeTrunk(Object):
    textures =[
         BGL.assets.get('KT-forest/texture/treetrunk'),
         BGL.assets.get('KT-forest/texture/shrub0000'),
         BGL.assets.get('KT-forest/texture/shrub0001'),
         BGL.assets.get('KT-forest/texture/shrub0002'),
         BGL.assets.get('KT-forest/texture/shrub0003')
    ]

    def parse(od,df):

        x1 = float(od["x"])
        y1 = float(od["y"])

        x2 = float(od["w"])
        y2 = float(od["h"])

        cx = (x1+x2) / 2.0
        cy = (y1+y2) / 2.0
      
        w = (x2-x1)*0.5
        h = (y2-y1)*0.5

        return TreeTrunk(
            p=[cx,cy],
            size=[w,h],
            scale_uv=[1.0,1.0],
            tick_type = Object.TickTypes.STATIC,
            visible = True,
            buftarget = "floor",
            texture = choice(TreeTrunk.textures)
            )