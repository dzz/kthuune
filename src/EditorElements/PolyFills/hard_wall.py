from .Factory import Factory

class hard_wall:
    layer = 3
    def reduce(area, brush):
        Factory.make_edges( area,
            [
                [ brush.x1, brush.y1, brush.x2, brush.y1 ], 
                [ brush.x1, brush.y2, brush.x2, brush.y2 ], 
                [ brush.x1, brush.y1, brush.x1, brush.y2 ],
                [ brush.x2, brush.y1, brush.x2, brush.y2 ],
            ],
            True, True, False)




        
