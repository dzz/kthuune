from .Factory import Factory
from random import choice
from .WorldSpaceBrush import WorldSpaceBrush
from .layer_map import layer_map

class lantern:
    dims = None
    mesh_key = "platform"
    layer = layer_map.get_layer_id("decorator")

    def reduce(area, brush):
        wsb = WorldSpaceBrush.from_brush(brush) 
        Factory.make_lantern( area, wsb.cx, wsb.cy)




