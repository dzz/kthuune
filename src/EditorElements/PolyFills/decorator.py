from .Factory import Factory
from random import choice
from .WorldSpaceBrush import WorldSpaceBrush
from .layer_map import layer_map

class decorator:
    dims = None
    mesh_key = None
    layer = layer_map.get_layer_id("decorator")

    def reduce(area, brush):
        wsb = WorldSpaceBrush.from_brush(brush) 
        Factory.make_decorator( area, brush.decorator_id, wsb.x1,wsb.y1,wsb.x2,wsb.y2, brush.self_lit )



