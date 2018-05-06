from Newfoundland.Object import Object
from Beagle import API as BGL
from math import sin,cos
from ..LevelProps.SpeechBubble import SpeechBubble
from random import choice

class Elder(Object):
    texture = BGL.assets.get('KT-player/texture/elder0000')
    #texture = BGL.assets.get('KT-forest/texture/cave_entrance')

    def parse(od,df):
        o = Elder( p = [ od["x"], od["y"] ] )
        return o 

    def customize(self):
        self.texture = Elder.texture
        #self.buftarget = "popup"
        self.buftarget = "popup"
        self.size =  [ 6.0, 6.0 ]
        self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
        self.light_color =  [ 1.0,0.4,0.4,1.0]
        self._t = 0.0 
        self.physics = { "radius" : 2.0, "mass"   : 100.0, "friction" : 0.0 } 
        self.tick_type = Object.TickTypes.TICK_FOREVER
        self.z_index = 1
        self.sensed = False
        self.talking = False
        #self.script = [
        #    "I see you, vectorlord",
        #    "you must find your sword."
        #]
        self.script = Elder.script
        self.floor_script = Elder.floor_script
        self.script_item = -1
        self.script_t = 0
        self.script_char = 1

    def tick(self):

        if self.talking:
            msg = self.script[self.script_item]
            self.tooltip = msg[0:self.script_char]
            if(self.script_t%4==0):
                if(self.script_char < len(msg)):
                    self.script_char += 1
            self.script_t -= 1
            if(self.script_t<=0):
                self.script_item = self.script_item+1
                self.script_char = 1
                if self.script_item == len(self.script):
                    self.talking = False
                    self.tooltip = None
                else:
                    self.script_t = len(self.script[self.script_item]) * 12
                

        if not self.sensed:
            dx = self.p[0] - self.floor.player.p[0]
            dy = self.p[1] - self.floor.player.p[1]

            dst = (dx*dx+dy*dy)

            if(dst<30):
                self.sensed = True
                self.talking = True
                SpeechBubble.instance.set_script(self.floor_script,  self.p)
            ###    self.floor.player.set_hud_message("HELLO I TALK")
            ###    if self.floor.player.get_pad().button_down( BGL.gamepads.buttons.X ):
            ###        pass
        else:
            self._t += 0.01
            self.light_radius = (sin(self._t)*25)+35
