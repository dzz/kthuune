from .Factory import Factory
from random import choice
from .WorldSpaceBrush import WorldSpaceBrush
from .layer_map import layer_map

class playerstart:
    dims = (3,3)
    mesh_key = "platform"
    layer = layer_map.get_layer_id("totem")

    def reduce(area, brush):
        wsb = WorldSpaceBrush.from_brush(brush) 
        #Factory.make_totem( area, wsb.cx, wsb.cy)
        Factory.make_playerstart( area, wsb.cx, wsb.cy)
        area.nodefault_playerstart = True

        for x in range(brush.x1, brush.x2):
            for y in range(brush.y1, brush.y2):
                area.set_tile(x,y, choice(range(43,47)))

        for x in range(brush.x1-1, brush.x2+1):
                area.set_conditional_tile(x,brush.y1-1, choice(range(30,42)))
        for x in range(brush.x1-1, brush.x2+1):
                area.set_conditional_tile(x,brush.y2, choice(range(30,42)))
        for y in range(brush.y1-1, brush.y2+1):
                area.set_conditional_tile(brush.x1-1,y, choice(range(30,42)))
        for y in range(brush.y1-1, brush.y2+1):
                area.set_conditional_tile(brush.x2,y, choice(range(30,42)))



