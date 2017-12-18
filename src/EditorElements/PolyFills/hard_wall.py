from .Factory import Factory

class hard_wall:
    def reduce(area, brush):
        Factory.make_edges( area,
            [
                [ brush.x1, brush.y1, brush.x2, brush.y1 ], 
                [ brush.x1, brush.y2, brush.x2, brush.y2 ], 
                [ brush.x1, brush.y1, brush.x1, brush.y2 ],
                [ brush.x2, brush.y1, brush.x2, brush.y2 ],
            ],
            True, True, False)




        
