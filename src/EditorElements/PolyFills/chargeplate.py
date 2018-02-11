from .Factory import Factory
from random import choice
from .WorldSpaceBrush import WorldSpaceBrush
from .layer_map import layer_map

class chargeplate:
    dims = (2,2)
    mesh_key = "platform"
    layer = layer_map.get_layer_id("floor_interactions")

    def reduce(area, brush):
        wsb = WorldSpaceBrush.from_brush(brush) 
        Factory.make_chargeplate( area, wsb.cx, wsb.cy, brush.group)
        Factory.make_light( area, wsb.cx, wsb.cy, "shortwave" )



