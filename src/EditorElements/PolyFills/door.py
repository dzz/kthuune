from ..Brushes import Brushes
from .WorldSpaceBrush import WorldSpaceBrush
from .Factory import Factory
from .Edges import Edges
from random import choice
import uuid

class door:
    layer = 3
    dims = None
    mesh_key = "platform"
    def reduce( area, brush ):
        for x in range(brush.x1, brush.x2):
            for y in range(brush.y1, brush.y2):
                area.set_tile(x,y, choice(range(3,5)))

        wsb = WorldSpaceBrush.from_brush(brush) 

        horizontal = False
        if(wsb.width> wsb.height):
            horizontal = True

        door_name = str(uuid.uuid1())

        if horizontal:
            Factory.make_door( area, wsb.x1, wsb.cy, wsb.x2, wsb.cy, door_name )
        else:
            Factory.make_door( area, wsb.cx, wsb.y1, wsb.cx, wsb.y2, door_name )

        Factory.make_light( area, wsb.cx, wsb.cy, "shortwave" )
        #edges = Edges.make_edges( area,brush, Brushes.brushes )
        #Factory.make_edges( area, edges )

