from .Factory import Factory
from random import choice
from .WorldSpaceBrush import WorldSpaceBrush
from .layer_map import layer_map

class treetrunk:
    dims = None
    mesh_key = None
    layer = layer_map.get_layer_id("floor_interactions")

    def reduce(area, brush):
        wsb = WorldSpaceBrush.from_brush(brush) 
        Factory.make_treetrunk( area, wsb.x1,wsb.y1,wsb.x2,wsb.y2 )



