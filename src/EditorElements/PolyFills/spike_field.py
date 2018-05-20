from .Factory import Factory
from random import choice
from .WorldSpaceBrush import WorldSpaceBrush
from .layer_map import layer_map

class spike_field:
    dims = None
    mesh_key = None
    layer = layer_map.get_layer_id("hazards")

    def reduce(area, brush):
        wsb = WorldSpaceBrush.from_brush(brush) 
        Factory.make_spikes( area, brush )




