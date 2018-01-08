import importlib
from .PolyFills.platform_floor import platform_floor
from .PolyFills.checker_floor import checker_floor
from .PolyFills.hard_wall import hard_wall
from .PolyFills.soft_wall import soft_wall
from .PolyFills.church_wall import church_wall
from .PolyFills.totem import totem
from .PolyFills.lantern import lantern
from .PolyFills.door import door
from .PolyFills.skeline import skeline
from .PolyFills.trees import trees
from .PolyFills.hostage_field import hostage_field
from .PolyFills.chargeplate import chargeplate
from .PolyFills.firepot_x import firepot_x
from .PolyFills.firepot_y import firepot_y

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
                "checker_floor" : checker_floor,
                "hard_wall" : hard_wall,
                "soft_wall" : soft_wall,
                "church_wall" : church_wall,
                "totem" : totem,
                "lantern" : lantern,
                "door" : door,
                "skeline" : skeline,
                "trees" : trees,
                "hostage_field": hostage_field,
                "chargeplate" : chargeplate,
                "firepot_x" : firepot_x,
                "firepot_y" : firepot_y,
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
    
