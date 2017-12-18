from Beagle import API as BGL
from .EditorElements.Cursor import Cursor
from .EditorElements.Grid import Grid
from .EditorElements.TitleBar import TitleBar
from .EditorElements.ToolBox import ToolBox
from .EditorElements.BrushTool import BrushTool
from .EditorElements.Brushes import Brushes
from .EditorElements.BrushSelectTool import BrushSelectTool
from .EditorElements.World import World
from .EditorElements.LevelPreview import LevelPreview
from .EditorElements.WorldCursor import WorldCursor

class Editor:
    instance = None
    ui_fb = BGL.framebuffer.from_dims(960, 540)
    cursor_tex = BGL.assets.get('KT-player/texture/cursor')

    def __init__(self):
        Editor.instance = self
        self.mouse_context = "camera"
        self.camera_x = 0
        self.camera_y = 0
        self.camera_zoom = 1.0
        self.mx = 0
        self.my = 0
        self.nmx = 0
        self.nmy = 0
        self.wmx = 0
        self.wmy = 0
        self.layer = 0
        self.show_preview = True
        self.show_brushes = True
        pass

    def toggle_preview():
        Editor.instance.show_preview = not Editor.instance.show_preview

    def toggle_brushes():
        Editor.instance.show_brushes = not Editor.instance.show_brushes

    def layer_down():
        Editor.instance.layer = max( 0, Editor.instance.layer - 1)

    def layer_up():
        Editor.instance.layer = Editor.instance.layer + 1


    def scr_to_world(self, x, y):
        x = x * (1.0/Grid.zoom)
        y = y * (1.0/Grid.zoom)

        x+= Grid.cx
        y+= Grid.cy
        return ( x, y )

    def world_to_scr(self, x, y):
        x-= Grid.cx
        y-= Grid.cy

        x = x / (1.0/Grid.zoom)
        y = y / (1.0/Grid.zoom)
        return ( x, y )

    def size_to_scr(self, size):
        return size / (1.0/Grid.zoom)
        
    def dispatch_mousewheel(self,y):
        if(self.mouse_context == "camera"):
            self.camera_zoom += (y*0.1)
            if(self.camera_zoom<0.1):
                self.camera_zoom = 0.1

    def dispatch_mousedown(self,button,x,y):

        if(self.mouse_context == "toolbox"):
            ToolBox.dispatch_mousedown(self, button, x,y)

        if(self.mouse_context == "camera"):
            if(button ==1):
                if(BrushTool.is_defining()):
                    BrushTool.end_brush()
                else:
                    BrushSelectTool.attempt_select(self)
                    if(len(Brushes.selected_brushes) == 0):
                        BrushTool.start_brush(self)

            if(button ==2):
                origin_x, origin_y = self.scr_to_world(self.nmx,self.nmy)
    
                self.camera_x = origin_x;
                self.camera_y = origin_y;
    
        pass
 
    def dispatch_mouseup(self,button,x,y):
        pass
 
    def dispatch_mousemotion(self,x,y):
        if(self.mouse_context == "toolbox"):
            ToolBox.dispatch_mousemotion(self, x,y)
        pass

    def configure(self, config):
        pass

    def init(self):
        pass

    def update_mouse_position(self):
        ( self.mx, self.my ) = BGL.engine.get_mouse_state()
        self.nmx = ((self.mx / BGL.engine.window.width)*16)-8
        self.nmy = ((self.my / BGL.engine.window.height)*9)-4.5
        self.wmx, self.wmy = self.scr_to_world(self.nmx, self.nmy)
        if(ToolBox.is_open()) and (self.nmx < -4.8):
                self.mouse_context = "toolbox"
        else:
                self.mouse_context = "camera"

    def tick(self):
        LevelPreview.tick(self)
        self.update_mouse_position()
        if BrushTool.is_defining():
            BrushTool.update_brush()
        pass

    def get_title_str(self):
        return "EDITOR. screen({0:0.2f},{1:0.2f}, world({2:0.2f},{3:0.2f})".format( self.nmx, self.nmy, self.wmx, self.wmy)
    def get_status_str(self):
        return "LAYER:{0}".format( self.layer)

    def render(self):
        with BGL.context.render_target(Editor.ui_fb):
            BGL.context.clear(0.0,0.0,0.0,0.0)
            with BGL.blendmode.alpha_over:

                ToolBox.render(self)
                TitleBar.render(self)
                BGL.lotext.render_text_pixels(self.get_title_str(), 2,1, [0.3,0.3,0.3])
                BGL.lotext.render_text_pixels(self.get_title_str(), 2,2, [1.0,1.0,1.0])
                BGL.lotext.render_text_pixels(self.get_status_str(), 2,540-11, [0.3,0.3,0.3])
                BGL.lotext.render_text_pixels(self.get_status_str(), 2,540-10, [1.0,1.0,1.0])


        BGL.context.clear(0.0,0.0,0.0,0.0)
        Grid.render(self)
        if(self.show_preview):
            LevelPreview.render(self)

        if(self.show_brushes):
            Brushes.render_rects(self)
            Brushes.render_labels(self)
        BrushTool.render(self)
        with BGL.blendmode.add:
            WorldCursor.render(self)
        with BGL.blendmode.alpha_over:
            Editor.ui_fb.render_processed(BGL.assets.get("beagle-2d/shader/passthru"))
        with BGL.blendmode.alpha_over:
            Cursor.render(self)


    def finalize(self):
        pass


BGL.keyboard.register_keydown_handler('p', World.reduce)
BGL.keyboard.register_keydown_handler('b', Editor.toggle_brushes)
BGL.keyboard.register_keydown_handler('v', Editor.toggle_preview)
BGL.keyboard.register_keydown_handler('leftbracket', Editor.layer_down)
BGL.keyboard.register_keydown_handler('rightbracket', Editor.layer_up)
