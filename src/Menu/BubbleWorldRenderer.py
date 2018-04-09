from Beagle import API as BGL

class BubbleWorldRenderer():
    primitive = BGL.primitive.unit_uv_square
    textures = BGL.assets.get('KT-player/animation/worldbubble')
    shader = BGL.assets.get('KT-player/shader/worldbubble')
    view = BGL.view.widescreen_16_9
    texture_idx = 0
    frt = 0
    visible = False

    def reset():
        BubbleWorldRenderer.texture_idx = 0
        BubbleWorldRenderer.visible = True

    def tick():
        BubbleWorldRenderer.frt += 1
        if(BubbleWorldRenderer.frt == 2):
            BubbleWorldRenderer.frt = 0
        else:
            return

        if(BubbleWorldRenderer.texture_idx < (len(BubbleWorldRenderer.textures)-1)):
            BubbleWorldRenderer.texture_idx += 1
            BubbleWorldRenderer.visible = True
        else:
            BubbleWorldRenderer.visible = False



    def render():

        if not BubbleWorldRenderer.visible:
            return

        with BGL.blendmode.alpha_over:
            BubbleWorldRenderer.primitive.render_shaded( BubbleWorldRenderer.shader, {
                "translation_local" : [ 0.0, 0.0 ],
                "scale_local" : [ 1.0, 1,0 ],
                "translation_world" : [ 0.0,0.0 ],
                "scale_world" : [ 1.0,1.0 ],
                "view" : BubbleWorldRenderer.view,
                "rotation_local" : 0.0,
                "filter_color" : [ 1.0,1.0,1.0,1.0],
                "uv_translate" : [ 0.0,0.0],
                "texBuffer" : BubbleWorldRenderer.textures[BubbleWorldRenderer.texture_idx] }
            )




