from Newfoundland.Object import Object
from Beagle import API as BGL
from math import sin,cos
from .SpeechBubble import SpeechBubble
from ...Abilities import Abilities
from ..Locomotion.Totem import Totem
from ...KSounds import KSounds

class Telekine(Object):
    instance = None
    BirdmanTextures = [
        BGL.assets.get("KT-player/texture/birdman0000"),
        BGL.assets.get("KT-player/texture/birdman0001"),
        BGL.assets.get("KT-player/texture/birdman0002")
    ]
    def parse(od,df):
        Telekine.instance = Telekine(p=[od["x"],od["y"]])
        return Telekine.instance

    def customize(self):
        self.buftarget = "floor"
        self.texture = Telekine.BirdmanTextures[0]
        self.tick_type = Object.TickTypes.TICK_FOREVER
        self.size = [2.0,2.0]
        self.color = [ 1.0,1.0,1.0,0.0]
        self.fr = 0 
        self.light_color = [ 0.0,0.6,0.9,1.0 ]
        self.light_radius = 1
        self.visible = False

        if Abilities.TelekineInstalled:
            self.visible = True
            self.light_radius = 25
            self.color[3] = 1.0

    def enable(self):
        def spawn_objects():
            t = None
            for x in range(0,3):
                t = Totem( p = [ self.p[0]+7.5+23 + (x*10), self.p[1] + 4.5 ])
                self.floor.snap_enemies.append(t)
                self.floor.create_object(t)
                t.sleep_totem()
                t.reset_timer -= x*45
                self.floor.camera.grab_cinematic( t, 170+(45*3) )

            sb = SpeechBubble( p = list(self.p) )
            sb.trigger_script = [ "HEY! BASTARD!", "PUSH (X) TO TELEKINE" ]
            sb.mode = 1
            self.floor.create_object( sb )
            sb.tick()
            sb.p[0] = self.p[0] + 17.5+23
            sb.p[1] = self.p[1] + 6.5

        self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
        self.visible = True
        self.get_camera().grab_cinematic(self, 200, spawn_objects )
        Abilities.TelekineInstalled = True

    def tick(self):

        if(self.visible):
            if(self.color[3]<1.0):
                self.color[3] += 0.01
            if(self.light_radius < 25 ):
                self.light_radius += 0.2

        self.fr += 1
        if(self.fr == 90):
            self.fr = 0
        self.texture = Telekine.BirdmanTextures[ self.fr // 30 ]
