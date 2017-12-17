from Beagle import API as BGL

class ToolBox:
    shader = BGL.assets.get('KT-editor/shader/toolbox')
    primitive = BGL.primitive.unit_uv_square

    open_amt = 0.0
    open_tgt = 0.0

    def is_open():
        return ToolBox.open_tgt == 1.0

    def toggle():
        if(ToolBox.open_tgt == 0.0):
            ToolBox.open_tgt = 1.0
        else:
            ToolBox.open_tgt =0.0

    def render(app):
        ToolBox.open_amt = (ToolBox.open_amt*0.8)  + (ToolBox.open_tgt*0.2)
        ToolBox.primitive.render_shaded( ToolBox.shader, { "open_amt" : ToolBox.open_amt } )

    def dispatch_mousedown(app, button, x, y):
        return


BGL.keyboard.register_keydown_handler('tab', ToolBox.toggle)
