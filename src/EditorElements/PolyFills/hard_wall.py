from .Factory import Factory
from random import choice

class hard_wall:
    layer = 3
    dims = None
    mesh_key = None

    def reduce(area, brush):
        Factory.make_edges( area,
            [
                [ brush.x1, brush.y1, brush.x2, brush.y1 ], 
                [ brush.x1, brush.y2, brush.x2, brush.y2 ], 
                [ brush.x1, brush.y1, brush.x1, brush.y2 ],
                [ brush.x2, brush.y1, brush.x2, brush.y2 ],
            ],
            True, True, False)
        for x in range(brush.x1, brush.x2):
            for y in range(brush.y1, brush.y2):
                area.set_tile(x,y, choice(range(10,15)), brush, True)




        
