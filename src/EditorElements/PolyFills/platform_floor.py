from .WorldSpaceBrush import WorldSpaceBrush
from .Factory import Factory
from .Edges import Edges
from .layer_map import layer_map

class platform_floor:
    layer = layer_map.get_layer_id("floor")
    dims = None
    mesh_key = "platform"
    def reduce( area, brush ):
        for x in range(brush.x1, brush.x2):
            for y in range(brush.y1, brush.y2):
                area.set_tile(x,y, 0)

        wsb = WorldSpaceBrush.from_brush(brush) 

        Factory.make_light( area, wsb.cx, wsb.cy, "shipfill" )


        
