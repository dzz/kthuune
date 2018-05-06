from Beagle import API as BGL
from .PolyFillList import PolyFillList
from .PolyFills.layer_map import layer_map
from .BrushFile import BrushFile
from .Brush import Brush

class Brushes:
    Brush = Brush
    ui_fb = BGL.framebuffer.from_dims(960, 540)
    brushes = []
    texture = BGL.assets.get('KT-editor/texture/brush')
    primitive = BGL.primitive.unit_uv_square
    shader = BGL.assets.get('beagle-2d/shader/beagle-2d')
    selected_brushes = []
    level_name = "default"
    w_sizes = [ 7.0, 14.0 ]
    w_size = 7.0
    difficulty = 0
    weight = 1
    
    def cycle_size():
        i = Brushes.w_sizes.index( Brushes.w_size )
        i = i +1 
        if(i>=len(Brushes.w_sizes)):
            i= 0
        Brushes.w_size = Brushes.w_sizes[i]

    def set_name(name):
        Brushes.level_name = name

    def save():
        BrushFile.save( Brushes )

    def load():
        BrushFile.load(Brushes)

    def by_layer(l):
        return list(filter(lambda x: x.layer == l,Brushes.brushes))

    def add_brush(brush):
        Brushes.brushes.append(brush)

    def select_none():
        Brushes.selected_brushes = []
    
    def remove_selected():
        for brush in Brushes.selected_brushes:
            Brushes.brushes.remove(brush)

    def reflow():
        for brush in Brushes.brushes:
            pf = PolyFillList.getPolyFill( brush.polyfill_key )
            brush.layer = pf.layer

    def collapse():
        for brush in Brushes.brushes:
            brush.layer = 0

    def render_labels(app):
        with BGL.context.render_target( Brushes.ui_fb ):
            BGL.context.clear( 0.0,0.0,0.0,0.0 )
            with BGL.blendmode.alpha_over:
                for brush in Brushes.brushes:
                        if brush.layer != app.layer:
                            continue
                        cx1, cy1 = app.world_to_scr( brush.x1, brush.y1)
                        cx2, cy2 = app.world_to_scr( brush.x2, brush.y2)
                        cnx = (cx1+cx2)/2
                        cny = (cy1+cy2)/2
                        cnx*=60
                        cny*=60
                        cnx += 480
                        cny += 270

                        if not brush.should_render_texture_name():
                            label = "{0}({1})".format(brush.polyfill_key, brush.group)
                            BGL.lotext.render_text_pixels( label, cnx-(len(label)*4), cny-8, [1.0,1.0,1.0])
                            BGL.lotext.render_text_pixels( label, cnx-(len(label)*4), cny, [0.0,0.0,0.0])
                        else:
                            if(brush.self_lit):
                                l = "L"
                            else:
                                l = ""
                            label = "*{0}*{1}".format(app.type.decorators[ brush.decorator_id ].animation_id,l )
                            BGL.lotext.render_text_pixels( label, cnx-(len(label)*4), cny, [0.0,0.0,0.0])
                            BGL.lotext.render_text_pixels( label, cnx-(len(label)*4), cny+1, [0.0,1.0,0.0])

        with BGL.blendmode.alpha_over:
            Brushes.ui_fb.render_processed(BGL.assets.get("beagle-2d/shader/passthru"))

    def set_polyfill(polyfill_key):
        for brush in Brushes.selected_brushes:
            brush.polyfill_key = polyfill_key

    def move_left():
        for brush in Brushes.selected_brushes:
            brush.x1 -=1
            brush.x2 -=1

    def move_right():
        for brush in Brushes.selected_brushes:
            brush.x1 +=1
            brush.x2 +=1

    def move_up():
        for brush in Brushes.selected_brushes:
            brush.y1 -=1
            brush.y2 -=1

    def move_down():
        for brush in Brushes.selected_brushes:
            brush.y1 +=1
            brush.y2 +=1

    def render_rects(app):
        with BGL.blendmode.add:
            for brush in Brushes.brushes:
                cx1, cy1 = app.world_to_scr( brush.x1, brush.y1)
                cx2, cy2 = app.world_to_scr( brush.x2, brush.y2)

                width =  (cx2-cx1)/2
                height = (cy2-cy1)/2

                cnx = (cx1+cx2)/2
                cny = (cy1+cy2)/2

                if brush in Brushes.selected_brushes:
                    filter_color = [ 0.7,0.7,0.7,0.7]
                else:
                    filter_color = [ 0.5,0.5,0.5,0.5]

                if brush.layer !=  app.layer:
                    filter_color = [ 0.2,0.2,0.2,0.2]

                Brushes.primitive.render_shaded(Brushes.shader, {
                    "texBuffer"            : Brushes.texture,
                    "translation_local"    : [ 0.0,0.0],
                    "scale_local"          : [ width,height],
                    "translation_world"    : [ cnx,cny ],
                    "scale_world"          : [ 1.0, 1.0 ],
                    "view"                 : BGL.view.widescreen_16_9,
                    "rotation_local"       : 0.0,
                    "filter_color"         : filter_color
                    })

