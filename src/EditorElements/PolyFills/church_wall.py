from .Factory import Factory
from random import choice
from .layer_map import layer_map
from .WorldSpaceBrush import WorldSpaceBrush
from random import uniform

class church_wall:
    layer = layer_map.get_layer_id("wall")
    dims = None
    mesh_key = None

    def reduce(area, brush):
        for x in range(brush.x1, brush.x2):
            for y in range(brush.y1, brush.y2):
                area.set_tile(x,y, choice(range(67,69)), brush, False)

        wsb = WorldSpaceBrush.from_brush(brush) 

        if(wsb.width >= 8) and (wsb.height >= 8 ):
                Factory.make_stainglass( area, wsb.cx, wsb.cy )
                Factory.make_light( area, wsb.cx, wsb.cy, "shipfill" )
        else:
                Factory.make_lantern( area, wsb.cx, wsb.cy)



        
