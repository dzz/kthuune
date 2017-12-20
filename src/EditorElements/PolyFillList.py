import importlib
from .PolyFills.room_test import room_test
from .PolyFills.hard_wall import hard_wall
from .PolyFills.totem import totem

class PolyFillList:
    cached_list = None

    def getPolyFillMap():
        if PolyFillList.cached_list is None:
            class no_polyfill():
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

    def getPolyFills():
        return list(PolyFillList.getPolyFillMap().keys())
    
