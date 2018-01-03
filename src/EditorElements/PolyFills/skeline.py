from .Factory import Factory
from random import choice
from .WorldSpaceBrush import WorldSpaceBrush
from .layer_map import layer_map

class skeline:
    dims = (3,3)
    mesh_key = "platform"
    layer = layer_map.get_layer_id("npc")

    def reduce(area, brush):
        wsb = WorldSpaceBrush.from_brush(brush) 
        Factory.make_skeline( area, wsb.cx, wsb.cy)




