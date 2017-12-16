from Beagle import API as BGL
from .EditorElements.Cursor import Cursor
from .EditorElements.Grid import Grid
from .EditorElements.TitleBar import TitleBar

class Editor:
    ui_fb = BGL.framebuffer.from_dims(960, 540)
    cursor_tex = BGL.assets.get('KT-player/texture/cursor')
    def __init__(self):


        self.mouse_context = "camera"
        self.camera_x = 0
        self.camera_y = 0
        self.camera_zoom = 1.0

        self.mx = 0
        self.my = 0
        self.nmx = 0
        self.nmy = 0
        pass
    
    def dispatch_mousewheel(self,y):
        if(self.mouse_context == "camera"):
            self.camera_zoom += (y*0.1)
            if(self.camera_zoom<0.1):
                self.camera_zoom = 0.1

    def dispatch_mousedown(self,button,x,y):
        pass
 
    def dispatch_mouseup(self,button,x,y):
        pass
 
    def dispatch_mousemotion(self,x,y):
    #    self.mx = x
    #    self.my = y
    #    self.nmx = ((self.mx / BGL.engine.window.width)*16)-8
    #    self.nmy = ((self.my / BGL.engine.window.height)*9)-4.5
        pass

    def configure(self, config):
        pass

    def init(self):
        pass

    def update_mouse_position(self):
        ( self.mx, self.my ) = BGL.engine.get_mouse_state()
        self.nmx = ((self.mx / BGL.engine.window.width)*16)-8
        self.nmy = ((self.my / BGL.engine.window.height)*9)-4.5

    def tick(self):
        self.update_mouse_position()
        pass

    def render(self):
        with BGL.context.render_target(Editor.ui_fb):
            BGL.context.clear(0.0,0.0,0.0,0.0)
            with BGL.blendmode.alpha_over:
                TitleBar.render(self)
                BGL.lotext.render_text_pixels("-=~ EDITOR =-~ {0:0.2f} {1:0.2f}".format(self.nmx, self.nmy), 1,1, [0.3,0.3,0.3])
                BGL.lotext.render_text_pixels("-=~ EDITOR =-~ {0:0.2f} {1:0.2f}".format(self.nmx, self.nmy), 1,2, [1.0,1.0,1.0])


        BGL.context.clear(0.0,0.0,0.0,0.0)
        Grid.render(self)
        with BGL.blendmode.alpha_over:
            Editor.ui_fb.render_processed(BGL.assets.get("beagle-2d/shader/passthru"))
        with BGL.blendmode.alpha_over:
            Cursor.render(self)

    def finalize(self):
        pass
