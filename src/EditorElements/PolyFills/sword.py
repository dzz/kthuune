from .Factory import Factory
from random import choice
from .WorldSpaceBrush import WorldSpaceBrush
from .layer_map import layer_map

class sword:
    dims = (2,2)
    mesh_key = "platform"
    layer = layer_map.get_layer_id("floor_interactions")

    def reduce(area, brush):
        wsb = WorldSpaceBrush.from_brush(brush) 
        Factory.make_sword( area, wsb.cx, wsb.cy  )
        Factory.make_light( area, wsb.cx, wsb.cy, "shortwave" )



