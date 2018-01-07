from .Factory import Factory
from random import choice
from .WorldSpaceBrush import WorldSpaceBrush
from .layer_map import layer_map

class trees:
    dims = None
    mesh_key = None
    layer = layer_map.get_layer_id("decorator")

    def reduce(area, brush):
        wsb = WorldSpaceBrush.from_brush(brush) 

        #if(wsb.width>wsb.height):
        #    edge = [ brush.x1, brush.y1, brush.x2, brush.y1 ]
        #else:
        #    edge = [ brush.x1,brush.y1, brush.x1, brush.y2 ]
    
        Factory.make_edges( area,
            [
                [ brush.x1, brush.y1, brush.x2, brush.y1 ], 
                [ brush.x1, brush.y2, brush.x2, brush.y2 ], 
                [ brush.x1, brush.y1, brush.x1, brush.y2 ],
                [ brush.x2, brush.y1, brush.x2, brush.y2 ],
            ], False,False,True)





