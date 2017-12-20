import importlib
from .PolyFills.room_test import room_test
from .PolyFills.hard_wall import hard_wall
from .PolyFills.totem import totem

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
                "room_test" : room_test,
                "hard_wall" : hard_wall,
                "totem" : totem,
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
    
