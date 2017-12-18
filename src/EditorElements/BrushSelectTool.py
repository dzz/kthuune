from Beagle import API as BGL
from .Brushes import Brushes
from .WorldCursor import WorldCursor

class BrushSelectTool:
    multi = False
    def enable_multi():
        BrushSelectTool.multi = True

    def disable_multi():
        BrushSelectTool.multi = False

    def attempt_select(app):
        valid = Brushes.by_layer(app.layer)
        for brush in valid:
            if WorldCursor.ix > brush.x1 and WorldCursor.ix < brush.x2 and WorldCursor.iy > brush.y1 and WorldCursor.iy < brush.y2:

                if(BrushSelectTool.multi):
                    Brushes.selected_brushes.append(brush)
                else:
                    Brushes.selected_brushes = [ brush ]
                return
        Brushes.selected_brushes = []

BGL.keyboard.register_keydown_handler('lshift', BrushSelectTool.enable_multi)
BGL.keyboard.register_keyup_handler('lshift', BrushSelectTool.disable_multi)
BGL.keyboard.register_keydown_handler('rshift', BrushSelectTool.enable_multi)
BGL.keyboard.register_keyup_handler('rshift', BrushSelectTool.disable_multi)
