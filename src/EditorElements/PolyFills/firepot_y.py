from .Factory import Factory
from .WorldSpaceBrush import WorldSpaceBrush
from .layer_map import layer_map

class firepot_y:
    layer = layer_map.get_layer_id("hazards")
    dims = None
    mesh_key = None

    def reduce(area, brush):
        wsb = WorldSpaceBrush.from_brush(brush) 

        for y in range(int(wsb.y1), int(wsb.y2), 6):
            Factory.make_firepot_right(area, y, wsb.y1)
            Factory.make_firepot_left(area, y+3, wsb.y2)




        
