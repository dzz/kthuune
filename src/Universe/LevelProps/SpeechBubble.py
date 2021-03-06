from Newfoundland.Object import Object
from Beagle import API as BGL
from ...KSounds import KSounds
from random import choice
import textwrap
from math import sin,cos

class ToolTip(Object): #must pass in message, width, owner
    
    def customize(self):
        if(len(self.message)<self.width):
            self.width = len(self.message)
        self.lines = textwrap.wrap( self.message, self.width )
        self.buffer = BGL.framebuffer.from_dims( self.width*8, len(self.lines)*8)
        self.texture = self.buffer
        with BGL.context.render_target(self.buffer):
            with BGL.blendmode.alpha_over:
                BGL.context.clear(0.0,0.0,0.0,1.0)
                for y,line in enumerate(self.lines):
                    BGL.lotext.render_text_pixels(line, 0,y*8, [ 1.0,1.0,1.0] )
        self.visible = True
        self.alive = True
        self.tick_type = Object.TickTypes.PURGING
        self.base_size = [ 0.5*self.width, -0.5*len(self.lines) ]
        self.size = list(self.base_size)
        self.t = 0

    def kill(self):
        self.alive = False

    def tick(self):
        self.t += 0.03
        self.rad = sin(self.t)*0.2
        return self.alive

    def get_shader_params(self):
        base_params = Object.get_shader_params(self)
        dx = self.owner.p[0] - self.floor.player.p[0]
        dy = self.owner.p[1] - self.floor.player.p[1]

        if self.owner.tooltip_layout==0:
            base_params['translation_world'][0] -= (self.owner.size[0]*1.2) * (1.0+(dx/30.))
            base_params['translation_world'][1] -= (self.owner.size[1]*1.2) * (1.0+(dy/30.))


        return base_params
        

class SpeechBubble(Object):

    def spawn(owner, script):
        bubble = SpeechBubble( triggered = True, visible = True, p = list(owner.p), mode = 1 ) 
        owner.floor.create_object(bubble)
        bubble.set_script( script, owner.p, False )

    scroll_in_chars = [
        "_",
        "-",
        "^",
        "."
    ]
    instance = None
    MODE_PERSISTANT_TRIGGERED = 1

    def parse(od,df):
        sb = SpeechBubble( p = [ od['x'], od['y'] ] )
        sb.trigger_script = [ od['meta']['text'] ]
        sb.mode = 1
        return sb

    def customize(self):
        self.mode = 0
        self.trigger_dist = 100
        self.triggered = False
        self.trigger_script = None

        self.buffer = BGL.framebuffer.from_dims( 8*20, 8*3)
        self.texture = self.buffer
        self.buftarget = "popup"
        self.tick_type = Object.TickTypes.TICK_FOREVER
        self.size = [ 8,-1.2 ]
        self.visible = False
        self.z_index = -9000
        self.script = None

        self.current_string = None
        self.current_string_timer = 0
        self.current_string_char = 0
        self.current_char_timer = 7
        self.script_queue = []
        self.t = 0.0

        
    def render_string(self, string):
        self.buffer = BGL.framebuffer.from_dims( 8*len(string) + 2, 10, filtered=False )
        self.texture = self.buffer
        self.size = [ 0.5*len(string),-0.8 ]
        with BGL.context.render_target( self.buffer ):
            BGL.context.clear( 0.0,0.0,0.0,1.0)
            with BGL.blendmode.alpha_over:
                BGL.lotext.render_text_pixels(string,1,0,[ 0.3,0.3,0.3 ])
                BGL.lotext.render_text_pixels(string,1,1,[ 0.5,0.0,0.9 ])

    def set_script(self,script, p, offs = True):

        if(self.script is None):
            self.script = script
            self.current_string = script[0]
            self.current_string_timer = 0

            self.p[0] = p[0]
            if offs:
                self.p[1] = p[1] + 7
            self.visible = True

    
    def next_char(self):
        if(self.current_string):
            if(self.current_string_char<=len(self.current_string)):
                KSounds.play(choice(KSounds.typewriter_keys))

                renderable_string = self.current_string[0:self.current_string_char]
                if(len(renderable_string) != len(self.current_string)):
                    renderable_string = renderable_string + SpeechBubble.scroll_in_chars[self.current_string_char%len(SpeechBubble.scroll_in_chars)]
                self.render_string( renderable_string )
                self.current_string_char+=1
                if(len(renderable_string)>=1):
                    tchar = renderable_string[-1]
                    if tchar == ",":
                        self.current_char_timer = choice([6,7])
                    elif tchar == "?":
                        self.current_char_timer = choice([8,9])
                    elif tchar in [".","!",":"]:
                        self.current_char_timer = choice([11,12])
                    else:
                        self.current_char_timer = choice([4,5,6])
            else:
                self.current_string_char = 0
                KSounds.play(KSounds.typewriter_return)
                self.current_char_timer = 2*len(self.current_string)
                if(len(self.script)>1):
                    self.current_string = self.script[1]
                    self.script = self.script[1:] 
                else:
                    self.script = None


    def tick(self):

        self.t+=0.06
        self.rad = sin(self.t)*0.03

        if(self.floor.player.title_card.displaying()):
            return

        if(self.mode == 1):
            if not self.triggered:
                dx = self.p[0] - self.floor.player.p[0]
                dy = self.p[1] - self.floor.player.p[1]
                md = (dx*dx)+(dy*dy)
                if(md<self.trigger_dist):
                    self.set_script( self.trigger_script, self.p )
                    self.triggered = True

        if(self.script):
            self.current_string_timer +=1
            if(self.current_string_timer > self.current_char_timer):
                self.current_string_timer = 0
                self.next_char()
        else:
            if(self.current_string_timer > self.current_char_timer):
                self.visible = False
                with BGL.context.render_target( self.buffer ):
                    BGL.context.clear( 0.0,0.0,0.0,0.0)

        #if(self.script):
        #    self.current_script_time += 1
        #pass            
