import importlib
from .PolyFills.room_test import room_test

class PolyFillList:
    cached_list = None

    def getPolyFillMap():
        if PolyFillList.cached_list is None:
            class no_polyfill():
                def reduce(area,brush):
                    pass
            polyfill_map = {
                "None" : no_polyfill,
                "room_test" : room_test
            }
            PolyFillList.cached_list = polyfill_map
        return PolyFillList.cached_list

    def getPolyFills():
        return list(PolyFillList.getPolyFillMap().keys())
    
