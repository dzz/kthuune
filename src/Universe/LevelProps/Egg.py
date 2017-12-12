from Newfoundland.Object import Object
from Beagle import API as BGL
from random import uniform, choice
from math import sin,cos
from ..Particles.SplatterParticle import SplatterParticle
from ..LevelEffects.Blood import Blood
from ...KSounds import KSounds
from .FloatingPlayer import FloatingPlayer
from ...Abilities import Abilities

class Egg(Object):
    slime_texture =  BGL.assets.get('KT-forest/texture/slime0small')
    def parse(od,df):
        Egg.instance = Egg(p=[od["x"],od["y"]])
        return Egg.instance
    frames = [
        BGL.assets.get('KT-forest/texture/egg1'),
        BGL.assets.get('KT-forest/texture/egg2'),
        BGL.assets.get('KT-forest/texture/egg3'),
        BGL.assets.get('KT-forest/texture/egg4'),
        BGL.assets.get('KT-forest/texture/egg5'),
        BGL.assets.get('KT-forest/texture/egg6'),
        BGL.assets.get('KT-forest/texture/egg7'),
        BGL.assets.get('KT-forest/texture/egg8'),
    ]
    def customize(self):
        self.buftarget = "floor"
        self.tick_type = Object.TickTypes.PURGING
        self.visible = True
        self.fr = 0
        self.fridx = 0
        self.texture = Egg.frames[0]
        self.size = [ 8.0,8.0 ]
        self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
        self.light_color = [ -1.0,1.0,-1.0,1.0 ]
        

    def tick(self):

        self.fridx += 1
        self.light_radius = 10+(cos(self.fridx/10)*5)
        if not self.floor.player.title_card.displaying():
            self.fr += 1

        self.floor.camera.grab_cinematic( self, 5 )

        if(self.fr<80):
            self.texture = Egg.frames[int(self.fr/10)]
            self.floor.player.visible = False

            if(self.fr>40):
                if(choice([True,False,False])):
                    KSounds.play(
                        choice([ 
                            KSounds.slimekill,
                            KSounds.slimecrush,
                            KSounds.enemy_killed
                        ]))
                if choice([True,False,False]):
                    self.floor.create_object(Blood(p=[self.p[0]+uniform(-3.0,3.0),self.p[1]+uniform(-3.0,3.0)]))
                for x in range(0,5):
                    self.floor.create_object( SplatterParticle( size = [ 5.0,5.0], ptexture = Egg.slime_texture, rad= uniform(0.0,6.5), p = [ self.p[0], self.p[1]]))
            return True

        else:
            self.floor.player.visible = True
            self.floor.objects.remove(self)
            self.floor.objects.remove(FloatingPlayer.instance)
            Abilities.Born = True
            return False
