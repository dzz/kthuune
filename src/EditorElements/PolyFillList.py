import importlib
from .PolyFills.platform_floor import platform_floor
from .PolyFills.hard_wall import hard_wall
from .PolyFills.soft_wall import soft_wall
from .PolyFills.church_wall import church_wall
from .PolyFills.totem import totem
from .PolyFills.lantern import lantern
from .PolyFills.door import door
from .PolyFills.skeline import skeline
from .PolyFills.trees import trees
from .PolyFills.generate_triggers import generate_below, generate_above, generate_left, generate_right

class PolyFillList:
    cached_list = None

    def getPolyFillMap():
        if PolyFillList.cached_list is None:
            class no_polyfill():
                layer = None
                dims = None
                mesh_key = None
                def reduce(area,brush):
                    pass
            polyfill_map = {
                "None" : no_polyfill,
                "platform_floor" : platform_floor,
                "hard_wall" : hard_wall,
                "soft_wall" : soft_wall,
                "church_wall" : church_wall,
                "totem" : totem,
                "lantern" : lantern,
                "door" : door,
                "skeline" : skeline,
                "trees" : trees,
                "generate_below" : generate_below,
                "generate_above" : generate_above,
                "generate_left" : generate_left,
                "generate_right" : generate_right,
            }
            PolyFillList.cached_list = polyfill_map
        return PolyFillList.cached_list

    def getPolyFill(key):
        return PolyFillList.getPolyFillMap()[key]

    def getPolyFills(layer = None):
        if not layer:
            return list(PolyFillList.getPolyFillMap().keys())
        else:
            return list(filter( lambda pf: PolyFillList.getPolyFill(pf).layer == None or PolyFillList.getPolyFill(pf).layer == layer, PolyFillList.getPolyFillMap().keys()))
    
