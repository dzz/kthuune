from .Factory import Factory
from .WorldSpaceBrush import WorldSpaceBrush
from .layer_map import layer_map

class firepot_x:
    layer = layer_map.get_layer_id("hazards")
    dims = None
    mesh_key = None

    def reduce(area, brush):
        wsb = WorldSpaceBrush.from_brush(brush) 

        for x in range(int(wsb.x1), int(wsb.x2), 6):
            Factory.make_firepot_down(area, x, wsb.y1)
            Factory.make_firepot_up(area, x+3, wsb.y2)




        
