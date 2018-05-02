from Beagle import API as BGL
from .WorldCursor import WorldCursor
from .Brushes import Brushes
from .Brush import Brush
from .PolyFillList import PolyFillList

class BrushTool:
    texture = BGL.assets.get('KT-editor/texture/brush')
    primitive = BGL.primitive.unit_uv_square
    shader = BGL.assets.get('beagle-2d/shader/beagle-2d')

    x1 = None
    y1 = None
    x2 = None
    y2 = None

    def cancel():
        BrushTool.x1 = None

    def is_defining():
        return BrushTool.x1 is not None

    def start_brush(app):
        BrushTool.x1 = WorldCursor.x
        BrushTool.y1 = WorldCursor.y
        BrushTool.layer = app.layer
        BrushTool.decorator_id = app.decorator_id

    def end_brush():
        if(BrushTool.x1-BrushTool.x2) == 0:
            return
        if(BrushTool.y1-BrushTool.y2) == 0:
            return
        if(BrushTool.x2<BrushTool.x1):
            tmp = BrushTool.x1
            BrushTool.x1 = BrushTool.x2
            BrushTool.x2 = tmp
        if(BrushTool.y2<BrushTool.y1):
            tmp = BrushTool.y1
            BrushTool.y1 = BrushTool.y2
            BrushTool.y2 = tmp
                    
        Brushes.add_brush(Brush.from_tool(BrushTool)) 
        BrushTool.x1 = None 

    def update_brush():

        polyfill = PolyFillList.getPolyFill( Brush.template_polyfill )

        if not polyfill.dims:
            BrushTool.x2 = WorldCursor.x
            BrushTool.y2 = WorldCursor.y
        else:
            BrushTool.x1 = WorldCursor.x
            BrushTool.y1 = WorldCursor.y
            BrushTool.x2 = WorldCursor.x+polyfill.dims[0]
            BrushTool.y2 = WorldCursor.y+polyfill.dims[1]

        if "snap" in polyfill.__dict__ and polyfill.snap:
            BrushTool.x1 = floor(BrushTool.x1 / polyfill.snap[0]) * polyfill.snap[0]
            BrushTool.x2 = floor(BrushTool.x2 / polyfill.snap[0]) * polyfill.snap[0]
            BrushTool.y1 = floor(BrushTool.y1 / polyfill.snap[1]) * polyfill.snap[1]
            BrushTool.y2 = floor(BrushTool.y2 / polyfill.snap[1]) * polyfill.snap[1]

        #if polyfill.align:
        #    pass


    def render(app):
        if(BrushTool.is_defining()):
            cx1, cy1 = app.world_to_scr( BrushTool.x1, BrushTool.y1)
            cx2, cy2 = app.world_to_scr( BrushTool.x2, BrushTool.y2)

            width =  (cx2-cx1)/2
            height = (cy2-cy1)/2

            cnx = (cx1+cx2)/2
            cny = (cy1+cy2)/2
            
            with BGL.blendmode.add:
                BrushTool.primitive.render_shaded(BrushTool.shader, {
                    "texBuffer"            : BrushTool.texture,
                    "translation_local"    : [ 0.0,0.0],
                    "scale_local"          : [ width,height],
                    "translation_world"    : [ cnx,cny ],
                    "scale_world"          : [ 1.0, 1.0 ],
                    "view"                 : BGL.view.widescreen_16_9,
                    "rotation_local"       : 0.0,
                    "filter_color"         : [ 0.5,0.5,0.5,1.0 ]
                    })

BGL.keyboard.register_keydown_handler('escape', BrushTool.cancel)

