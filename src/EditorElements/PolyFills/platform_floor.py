from .WorldSpaceBrush import WorldSpaceBrush
from .Factory import Factory
from .Edges import Edges
from .layer_map import layer_map
from random import choice

class platform_floor:
    layer = layer_map.get_layer_id("floor")
    dims = None
    mesh_key = "platform"
    def reduce( area, brush ):
        for x in range(brush.x1, brush.x2):
            for y in range(brush.y1, brush.y2):
                determinant = ((x*x)+(y*y) / 3.6)
                area.set_tile(x,y, 0)
                if(determinant > 20):
                    area.set_tile(x,y, choice([0,0,0,1,0,0,0,2,0,0,1,0]))
                if(determinant > 40):
                    area.set_tile(x,y, choice([0,1,0,1,0,2,0,2,0,0,1,0]))
                if(determinant > 60):
                    area.set_tile(x,y, choice([0,1,3,1,4,2,0,2,0,0,1,0]))
                if(determinant > 80):
                    area.set_tile(x,y, choice([2,1,3,1,4,2,0,2,1,0,1,5]))

        wsb = WorldSpaceBrush.from_brush(brush) 
        Factory.make_light( area, wsb.cx, wsb.cy, "shipfill" )

