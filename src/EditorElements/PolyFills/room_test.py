from ..Brushes import Brushes
from .WorldSpaceBrush import WorldSpaceBrush
from .Factory import Factory

class room_test:
    def reduce( area, brush ):
        for x in range(brush.x1, brush.x2):
            for y in range(brush.y1, brush.y2):
                area.set_tile(x,y, 0)

        wsb = WorldSpaceBrush.from_brush(brush) 

        Factory.make_light( area, wsb.cx, wsb.cy, "shipfill" )

        
