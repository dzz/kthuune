from Beagle import API as BGL
from .EditorElements.Cursor import Cursor
from .EditorElements.Grid import Grid
from .EditorElements.TitleBar import TitleBar
from .EditorElements.ToolBox import ToolBox
from .EditorElements.BrushTool import BrushTool
from .EditorElements.Brushes import Brushes
from .EditorElements.BrushFile import BrushFile
from .EditorElements.BrushSelectTool import BrushSelectTool
from .EditorElements.World import World
from .EditorElements.LevelPreview import LevelPreview
from .EditorElements.WorldCursor import WorldCursor
from .EditorElements.PolyFills.layer_map import layer_map
from .ParallaxBackground import ParallaxBackground
from .Abilities import Abilities

class Editor:
    instance = None
    ui_fb = BGL.framebuffer.from_dims(960, 540)
    cursor_tex = BGL.assets.get('KT-player/texture/cursor')
    decorators = BGL.assets.get('KT-forest/animation/decorators')
    show_grid = True

    def toggle_grid():
        if Editor.show_grid:
            Editor.show_grid = False
        else:
            Editor.show_grid = True

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
        self.decorator_id = 0
        self.type = Editor

        BGL.console.attach(self)
        pass


    def set_name(self,name):
        Brushes.set_name(name)

    def build_sequence(self,seqid):
        filename = "{0}/{1}.area".format(BGL.assets.get('KT-player/path/sequence'),seqid)
        f = open(filename,'w')
        f.write(World.GeneratedArea.output_data)
        f.close()
        Brushes.set_name(seqid)
        BrushFile.sequence = seqid
        Brushes.save()
        BrushFile.sequence = None

    def load_sequence(self,seqid):
        Brushes.set_name(seqid)
        BrushFile.sequence = seqid
        Brushes.load()
        BrushFile.sequence = None
        
    def save(self):
        Brushes.save()
    
    def load( self, name):
        Brushes.set_name(name)
        Brushes.load()

    def toggle_preview():
        Editor.instance.show_preview = not Editor.instance.show_preview

    def toggle_brushes():
        Editor.instance.show_brushes = not Editor.instance.show_brushes

    def layer_down():
        Brushes.selected_brushes = []
        Editor.instance.layer = max( 0, Editor.instance.layer - 1)

    def layer_up():
        Brushes.selected_brushes = []
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
        Abilities.Telekine = True
        Abilities.Dash = True
        
        LevelPreview.tick(self)
        self.update_mouse_position()
        if BrushTool.is_defining():
            BrushTool.update_brush()
        pass

    def get_decorator_str():
        return Editor.instance.decorators[ Editor.instance.decorator_id ].animation_id

    def get_title_str(self):
        return "EDITOR. screen({0:0.2f},{1:0.2f}, world({2:0.2f},{3:0.2f})".format( self.nmx, self.nmy, self.wmx, self.wmy)
    def get_status_str(self):
        if(self.layer > 0 and self.layer<len(layer_map.key_order)):
            layername = layer_map.key_order[self.layer]
        else:
            layername = self.layer

        gup_count = 0
        ptlen = 0
        stlen = 0
        if LevelPreview.floor:
            gup_count = LevelPreview.floor.gup_count
            ptlen = len(LevelPreview.floor.purging_tick_manager.tickables)
            stlen = len(LevelPreview.floor.simple_tick_manager.tickables)
        return "LAYER:{0} GFX_1:{1} PTLEN:{2} STLEN:{3}    DEC:{4}".format( layername, gup_count, ptlen, stlen, Editor.get_decorator_str() )

    def render(self):

        LevelPreview.synch_cams(self)

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

        Grid.render(self) # i don't really know why ( i mean..i probably do...) but this is required to update the camera

        if not Editor.show_grid:
            ParallaxBackground.render( (Grid.cx*2)*0.01 )

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

    def LevelGenerate():
        from .LevelGenerator import LevelGenerator
        LevelGenerator.generate()
    
    def set_group(x):
        for brush in Brushes.selected_brushes:
            brush.group = x

    def prev_decorator():
        Editor.instance.decorator_id = (Editor.instance.decorator_id - 1) % len(Editor.decorators)
        for brush in Brushes.selected_brushes:
            brush.decorator_id = Editor.instance.decorator_id

    def next_decorator():
        Editor.instance.decorator_id = (Editor.instance.decorator_id + 1) % len(Editor.decorators)
        for brush in Brushes.selected_brushes:
            brush.decorator_id = Editor.instance.decorator_id

    def toggle_lit():
        for brush in Brushes.selected_brushes:
            brush.self_lit = not brush.self_lit
        


BGL.keyboard.register_keydown_handler('p', World.reduce)
BGL.keyboard.register_keydown_handler('r', Brushes.cycle_size)
BGL.keyboard.register_keydown_handler('c', LevelPreview.toggle_camlock)
BGL.keyboard.register_keydown_handler('b', Editor.toggle_brushes)
BGL.keyboard.register_keydown_handler('v', Editor.toggle_preview)
BGL.keyboard.register_keydown_handler('leftbracket', Editor.layer_down)
BGL.keyboard.register_keydown_handler('rightbracket', Editor.layer_up)
BGL.keyboard.register_keydown_handler('escape', Brushes.select_none)
BGL.keyboard.register_keydown_handler('delete', Brushes.remove_selected)
BGL.keyboard.register_keydown_handler('a', Brushes.move_left)
BGL.keyboard.register_keydown_handler('d', Brushes.move_right)
BGL.keyboard.register_keydown_handler('w', Brushes.move_up)
BGL.keyboard.register_keydown_handler('s', Brushes.move_down)
BGL.keyboard.register_keydown_handler('f', Brushes.reflow)
BGL.keyboard.register_keydown_handler('r', Brushes.collapse)
#BGL.keyboard.register_keydown_handler('g', Editor.LevelGenerate)
BGL.keyboard.register_keydown_handler('g', Editor.toggle_grid)
BGL.keyboard.register_keydown_handler('l', Editor.toggle_lit)

BGL.keyboard.register_keydown_handler("0", lambda: Editor.set_group(0))
BGL.keyboard.register_keydown_handler("1", lambda: Editor.set_group(1))
BGL.keyboard.register_keydown_handler("2", lambda: Editor.set_group(2))
BGL.keyboard.register_keydown_handler("3", lambda: Editor.set_group(3))
BGL.keyboard.register_keydown_handler("4", lambda: Editor.set_group(4))
BGL.keyboard.register_keydown_handler("5", lambda: Editor.set_group(5))
BGL.keyboard.register_keydown_handler("6", lambda: Editor.set_group(6))
BGL.keyboard.register_keydown_handler("7", lambda: Editor.set_group(7))
BGL.keyboard.register_keydown_handler("8", lambda: Editor.set_group(8))
BGL.keyboard.register_keydown_handler("9", lambda: Editor.set_group(9))

BGL.keyboard.register_keydown_handler("comma", lambda: Editor.prev_decorator())
BGL.keyboard.register_keydown_handler("period", lambda: Editor.next_decorator())
