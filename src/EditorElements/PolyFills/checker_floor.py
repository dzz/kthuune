from .WorldSpaceBrush import WorldSpaceBrush
from .Factory import Factory
from .Edges import Edges
from .layer_map import layer_map
from random import choice

class checker_floor:
    layer = layer_map.get_layer_id("floor_decorators")
    dims = None
    mesh_key = "platform"
    def reduce( area, brush ):
        for x in range(brush.x1, brush.x2):
            for y in range(brush.y1, brush.y2):
                area.set_tile(x,y, choice(range(64,66)))

        wsb = WorldSpaceBrush.from_brush(brush) 

        Factory.make_light( area, wsb.cx, wsb.cy, "shipfill" )


