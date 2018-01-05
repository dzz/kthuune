from .Factory import Factory
from .WorldSpaceBrush import WorldSpaceBrush
from .layer_map import layer_map

class generate_below():
    mesh_key = None
    dims = None
    layer = layer_map.get_layer_id("g_trigger")

    def reduce(area,brush):
        wsb = WorldSpaceBrush.from_brush(brush)
        Factory.make_generator_below(area, wsb)

class generate_above():
    mesh_key = None
    dims = None
    layer = layer_map.get_layer_id("g_trigger")

    def reduce(area,brush):
        wsb = WorldSpaceBrush.from_brush(brush)
        Factory.make_generator_above(area, wsb)

class generate_left():
    mesh_key = None
    dims = None
    layer = layer_map.get_layer_id("g_trigger")

    def reduce(area,brush):
        wsb = WorldSpaceBrush.from_brush(brush)
        Factory.make_generator_left(area, wsb)

class generate_right():
    mesh_key = None
    dims = None
    layer = layer_map.get_layer_id("g_trigger")

    def reduce(area,brush):
        wsb = WorldSpaceBrush.from_brush(brush)
        Factory.make_generator_right(area, wsb)
