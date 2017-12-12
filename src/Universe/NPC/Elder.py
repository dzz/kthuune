from Newfoundland.Object import Object
from Beagle import API as BGL
from math import sin,cos

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

    def tick(self):
        self._t += 0.01
        self.light_radius = (sin(self._t)*85)+110
        dx = self.p[0] - self.floor.player.p[0]
        dy = self.p[1] - self.floor.player.p[1]

        dst = (dx*dx+dy*dy)

        #if(dst<30):
        #    SpeechBubble.instance.set_script(["Oh, it's you.", "Did you know that I talk?", "Yup... I talk.", "I write my text on the floor here, see?", "It's been... a while...","since I met youuuuuu","Ok bye."],  self.p)
        ###    self.floor.player.set_hud_message("HELLO I TALK")
        ###    if self.floor.player.get_pad().button_down( BGL.gamepads.buttons.X ):
        ###        pass
