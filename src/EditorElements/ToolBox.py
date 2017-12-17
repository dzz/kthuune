from Beagle import API as BGL

from .PolyFillMenu import PolyFillMenu

class ToolBox:
    menu = PolyFillMenu
    shader = BGL.assets.get('KT-editor/shader/toolbox')
    menu_shader = BGL.assets.get('KT-editor/shader/toolbox_menu')
    primitive = BGL.primitive.unit_uv_square
    contents_fb = BGL.framebuffer.from_dims(960,540)

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

        with BGL.context.render_target(ToolBox.contents_fb):
            BGL.context.clear(0.0,0.0,0.0,0.0)
            ToolBox.menu.render(app)

        ToolBox.contents_fb.render_processed(ToolBox.menu_shader, { "open_amt" : ToolBox.open_amt })
            

    def dispatch_mousedown(app, button, x, y):
        ToolBox.menu.dispatch_mousedown(app, button, x, y)
        return

    def dispatch_mousemotion(app, x, y):
        ToolBox.menu.dispatch_mousemotion(app, x, y)
        return


BGL.keyboard.register_keydown_handler('tab', ToolBox.toggle)
