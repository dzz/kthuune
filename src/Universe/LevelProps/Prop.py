from Newfoundland.Object import Object
from Beagle import API as BGL

#this is just a factory method for building static bitmaps to the game floor
class Prop(Object):
    def parse(pd):
        p = Prop( texture = BGL.assets.get("KT-props/texture/" + pd["image"]))
        p.p[0] = pd["x"]
        p.p[1] = pd["y"]
        p.size[0] = pd["w"]
        p.size[1] = pd["h"]
        p.r = pd["r"]

        if "layer" in pd and pd["layer"]==0:
            p.z_index = -1000
            p.buftarget="underfloor"
        else:
            p.buftarget = "floor"
            p.z_index = 1

        return p
