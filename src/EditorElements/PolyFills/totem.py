from .Factory import Factory
from random import choice
from .WorldSpaceBrush import WorldSpaceBrush

class totem:
    def reduce(area, brush):
        wsb = WorldSpaceBrush.from_brush(brush) 
        Factory.make_totem( area, wsb.cx, wsb.cy)

        for x in range(brush.x1, brush.x2):
            for y in range(brush.y1, brush.y2):
                area.set_tile(x,y, choice(range(40,47)))

        for x in range(brush.x1, brush.x2):
                area.set_tile(x,brush.y1, choice(range(36,40)))

        for x in range(brush.x1, brush.x2):
                area.set_tile(x,brush.y2, choice(range(36,40)))

        for y in range(brush.y1, brush.y2):
                area.set_tile(brush.x1,y, choice(range(36,40)))

        for y in range(brush.y1, brush.y2):
                area.set_tile(brush.x2,y, choice(range(36,40)))


