from Newfoundland.Object import Object
from Beagle import API as BGL
from ..Enemies.SnapEnemy import SnapEnemy
from ...KSounds import KSounds
from ..LevelEffects.AttackInfo import AttackInfo
from random import choice

from math import sin

class Totem(Object):
    alive_statements = [
        "~i'm alive~",
        "~hello~",
        "~greetings~",
        "~turned on~",
        "~hi~",
        "~breathing~",
        "~alive~",
        "~living~",
        "~activated~",
        "~existing~",
        "~awakened~",
        "~activated~",
        "~rising~",
        "~returning~",
        "~reentrance~" ]
    texture = BGL.assets.get('KT-forest/texture/totem')

    def customize(self):
        self.snap_type = SnapEnemy.TOTEM
        self.texture = Totem.texture
        self.buftarget = "popup"
        self.size =  [ 4.0, 4.0 ]
        self.tick_type = Object.TickTypes.TICK_FOREVER
        self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
        self.light_color =  [ 0.7,0.4,0.9,1.0]
        self.light_radius = 5
        #self.physics = { "radius" : 1.0, "mass"   : 100.0, "friction" : 0.0 } 
        self.physics = None
        self.z_index = 1
        self.anim_index = 0
        self.reset_timer = 0
        #self.group = 0
        self.active = True

    def tick(self):
        if self.active:
            self.reset_timer = self.reset_timer+1
        if(self.reset_timer == - 50):
            KSounds.play(KSounds.totem_restored)
        if(self.reset_timer==0):
            self.floor.snap_enemies.append(self)
            self.floor.create_object(AttackInfo( p=[ self.p[0], self.p[1] ], message=choice(Totem.alive_statements)))
            self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
            self.light_radius = 17
            self.visible = True
        self.anim_index += 0.1
        self.light_radius = 7 + (3*sin(self.anim_index))

    def sleep_totem(self):
        KSounds.play(KSounds.totem_hit)
        self.floor.snap_enemies.remove(self)

        self.reset_timer = -170

        self.visible = False
        self.light_type = Object.LightTypes.NONE
        self.active = False

        reset = True

        if self.group!=0:
            for totem in self.floor.totems:
                #print("TOTEM GROUP: {0}".format(totem.group))
                if totem.group == self.group and totem.active == True:
                    #print("totem breaking reset because group {0}=={1}".format(self.group, totem.group))
                    reset = False

        if reset:
            for totem in self.floor.totems:
                if totem.group == self.group:
                    totem.active = True

