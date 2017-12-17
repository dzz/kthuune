from Beagle import API as BGL

class Brushes:
    ui_fb = BGL.framebuffer.from_dims(960, 540)
    brushes = []
    texture = BGL.assets.get('KT-editor/texture/brush')
    primitive = BGL.primitive.unit_uv_square
    shader = BGL.assets.get('beagle-2d/shader/beagle-2d')

    def add_brush(brush):
        Brushes.brushes.append(brush)

    def render_labels(app):
        with BGL.context.render_target( Brushes.ui_fb ):
            BGL.context.clear( 0.0,0.0,0.0,0.0 )
            with BGL.blendmode.alpha_over:
                for brush in Brushes.brushes:
                        cx1, cy1 = app.world_to_scr( brush.x1, brush.y1)
                        cx2, cy2 = app.world_to_scr( brush.x2, brush.y2)
                        cnx = (cx1+cx2)/2
                        cny = (cy1+cy2)/2
                        cnx*=60
                        cny*=60
                        cnx += 480
                        cny += 270
                        BGL.lotext.render_text_pixels( "Boof", cnx, cny, [1.0,1.0,1.0])
        with BGL.blendmode.alpha_over:
            Brushes.ui_fb.render_processed(BGL.assets.get("beagle-2d/shader/passthru"))

    def render_rects(app):
        with BGL.blendmode.add:
            for brush in Brushes.brushes:
                cx1, cy1 = app.world_to_scr( brush.x1, brush.y1)
                cx2, cy2 = app.world_to_scr( brush.x2, brush.y2)

                width =  (cx2-cx1)/2
                height = (cy2-cy1)/2

                cnx = (cx1+cx2)/2
                cny = (cy1+cy2)/2
                Brushes.primitive.render_shaded(Brushes.shader, {
                    "texBuffer"            : Brushes.texture,
                    "translation_local"    : [ 0.0,0.0],
                    "scale_local"          : [ width,height],
                    "translation_world"    : [ cnx,cny ],
                    "scale_world"          : [ 1.0, 1.0 ],
                    "view"                 : BGL.view.widescreen_16_9,
                    "rotation_local"       : 0.0,
                    "filter_color"         : [ 1.0,1.0,1.0,1.0 ]
                    })
