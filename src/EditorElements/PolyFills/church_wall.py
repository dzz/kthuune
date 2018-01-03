from .Factory import Factory
from random import choice
from .layer_map import layer_map

class church_wall:
    layer = layer_map.get_layer_id("wall")
    dims = None
    mesh_key = None

    def reduce(area, brush):
        for x in range(brush.x1, brush.x2):
            for y in range(brush.y1, brush.y2):
                area.set_tile(x,y, choice(range(67,69)), brush, False)




        
