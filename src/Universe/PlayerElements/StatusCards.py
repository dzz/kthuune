from Beagle import API as BGL
from random import choice
from .Hud import Hud

class Bar():
    texbar1 = BGL.assets.get('KT-player/texture/bar1')
    texbar2 = BGL.assets.get('KT-player/texture/bar2')

class Card():
    shader = BGL.assets.get("KT-player/shader/card")
    primitive = BGL.primitive.unit_uv_square

    def __init__(self,player):
        self.real_impulse = 0.0
        self.flash_impulse = 0.0
        self.player = player
        self.statusamt = self.compute_value()
        self.impulse = 0.0
    

    def bar_tick(self):
        self.impulse *= 0.99
        self.flash_impulse *= 0.92
    
        if(self.flash_impulse<0.01):
            self.flash_impulse = 0.0

        self.fridx = (self.fridx + 1) %180
        last_value = self.statusamt
        self.statusamt = self.compute_value()
        if(self.statusamt!=last_value):
            if(self.statusamt < last_value):
                if(self.flash_impulse == 0.0):
                    self.flash_impulse = 1.0
            if(self.impulse<3.0):
                self.impulse += 1.0
        self.real_impulse = min( 1.0, self.impulse )

    def render(self):
        Card.primitive.render_shaded( Card.shader, self.get_shader_params() )

class HeartCard(Card):
    textures = [
            BGL.assets.get('KT-player/texture/heartcard0000'),
            BGL.assets.get('KT-player/texture/heartcard0001')
        ]
    #primitive = BGL.primitive.unit_uv_square
    def __init__(self, player):
        Card.__init__(self,player)
        self.fridx = choice( range(0,180) )

    def compute_value(self):
        return self.player.hp / 100

    def tick(self): 
        Card.bar_tick(self)

    def get_shader_params(self):
        return {
            "statusamt" : [ self.player.hp / 100.0 ],
            "statuscolor" : [ 1.0,0.0,0.0,1.0 ],
            "tick" : [ self.player.cardtick ],
            "impulse" : self.real_impulse,
            "flash_impulse" : self.flash_impulse,
            "texBuffer"            : Bar.texbar1,
            "translation_local"    : [ 0, 0 ],
            "scale_local"          : [ 4.0,1.0],
            "translation_world"    : [ 0.0,4.0 ],
            "scale_world"          : [1.0,1.0],
            "view"                 : Hud.view,
            "rotation_local"       : (self.real_impulse-0.5)*0.1,
            "filter_color"         : [1.0,1.0,1.0,1.0],
            "uv_translate"         : [ 0,0 ] }

class TelekineCard(Card):
    textures = [
            BGL.assets.get('KT-player/texture/swordcard0000'),
            BGL.assets.get('KT-player/texture/swordcard0001')
        ]
    #primitive = BGL.primitive.unit_uv_square
    def __init__(self, player):
        Card.__init__(self,player)
        self.fridx = choice( range(0,180) )

    def compute_value(self):
        return self.player.teleportAmt / 100.0

    def tick(self):
        Card.bar_tick(self)

    def get_shader_params(self):
        return {
            "statusamt" : [ self.statusamt ],
            "statuscolor" : [ 0.0,0.0,1.0,1.0 ],
            "tick" : [self.player.cardtick+10.0],
            "impulse" : self.real_impulse + self.player.telekineFlash,
            "flash_impulse" : self.flash_impulse + self.player.telekineFlash,
            "texBuffer"            : Bar.texbar2,
            "translation_local"    : [ 0, 0 ],
            "scale_local"          : [ 1.0, 0.4 ],
            "translation_world"    : [ -5.0,4.0],
            "scale_world"          : [1.0,1.0],
            "view"                 : Hud.view,
            "rotation_local"       : (self.real_impulse-0.5)*-0.1,
            "filter_color"         : [1.0,1.0,1.0,1.0],
            "uv_translate"         : [ 0,0 ] }

class SwordCard(Card):
    textures = [
            BGL.assets.get('KT-player/texture/swordcard0000'),
            BGL.assets.get('KT-player/texture/swordcard0001')
        ]
    #primitive = BGL.primitive.unit_uv_square
    def __init__(self, player):
        self.fridx = choice( range(0,180) )
        Card.__init__(self,player)

    def compute_value(self):
        return self.player.run_stamina / 100.0

    def tick(self):
        Card.bar_tick(self)

    def get_shader_params(self):
        return {
            "statusamt" : [ self.statusamt ],
            "statuscolor" : [ 0.0,1.0,0.0,1.0 ],
            "tick" : [self.player.cardtick+10.0],
            "impulse" : self.real_impulse,
            "flash_impulse" : self.flash_impulse,
            "texBuffer"            : Bar.texbar2,
            "translation_local"    : [ 0, 0 ],
            "scale_local"          : [ 1.0, 0.4 ],
            "translation_world"    : [ 5.0,4.0],
            "scale_world"          : [1.0,1.0],
            "view"                 : Hud.view,
            "rotation_local"       : (self.real_impulse-0.5)*-0.1,
            "filter_color"         : [1.0,1.0,1.0,1.0],
            "uv_translate"         : [ 0,0 ] }

class WandCard(Card):
    textures = [
            BGL.assets.get('KT-player/texture/wandcard0000'),
            BGL.assets.get('KT-player/texture/wandcard0001')
        ]
    #primitive = BGL.primitive.unit_uv_square
    def __init__(self, player):
        self.fridx = choice( range(0,180) )
        self.player = player

    def tick(self):
        self.fridx = (self.fridx + 1) %180

    def get_shader_params(self):

        return {
            "statusamt" : [ 1.0 ],
            "statuscolor" : [ 0.0,0.0,1.0,1.0 ],
            "tick" : [self.player.cardtick+40.0],
            "texBuffer"            : WandCard.textures[int(self.fridx/90)],
            "translation_local"    : [ 0, 0 ],
            "scale_local"          : [ 1.0*0.4,1.5*0.4],
            "translation_world"    : [ 7.5,-1.25],
            "scale_world"          : [1.0,1.0],
            "view"                 : Hud.view,
            "rotation_local"       : 0.0,
            "filter_color"         : [1.0,1.0,1.0,1.0],
            "uv_translate"         : [ 0,0 ] }

#class TelekineCard(Card):
#    shader = BGL.assets.get("KT-player/shader/telekine")
#    textures = [
#            BGL.assets.get('KT-player/texture/birdman0000'),
#            BGL.assets.get('KT-player/texture/birdman0001'),
#            BGL.assets.get('KT-player/texture/birdman0002'),
#            BGL.assets.get('KT-player/texture/birdman0001')
#        ]
#
#    def render(self):
#        with BGL.blendmode.alpha_over:
#            Card.primitive.render_shaded( TelekineCard.shader, self.get_shader_params() )
#
#    def __init__(self, player):
#        self.fridx = choice( range(0,360) )
#        self.player = player
#
#    def tick(self):
#        self.fridx = (self.fridx + 1) %360
#
#    def get_shader_params(self):
#        return {
#            "flashamt" : [ self.player.telekineFlash ],
#            "statusamt" : [ self.player.teleportAmt / 100.0 ],
#            "statuscolor" : [ 1.0,1.0,1.0,1.0 ],
#            "tick" : [self.player.cardtick+40.0],
#            "texBuffer"            : TelekineCard.textures[self.fridx//90],
#            "translation_local"    : [ 0, 0 ],
#            "scale_local"          : [ 0.7,0.7 ],
#            "translation_world"    : [ -7.0,3.2],
#            "scale_world"          : [1.0,1.0],
#            "view"                 : Hud.view,
#            "rotation_local"       : 0.0,
#            "filter_color"         : [1.0,1.0,1.0,1.0],
#            "uv_translate"         : [ 0,0 ] }

class PotionCard(Card):
    shader = BGL.assets.get("KT-player/shader/potion")
    textures = [
            BGL.assets.get('KT-player/texture/healthvial0000'),
            BGL.assets.get('KT-player/texture/healthvial0001'),
        ]

    def render(self):
        with BGL.blendmode.alpha_over:
            Card.primitive.render_shaded( PotionCard.shader, self.get_shader_params() )

    def __init__(self, player):
        self.fridx = choice( range(0,180) )
        self.player = player

    def tick(self):
        self.fridx = (self.fridx + 1) %180

    def get_shader_params(self):
        return {
            "flashamt" : [ self.player.potionFlash ],
            "statusamt" : [ 1.0 ],
            "statuscolor" : [ 1.0,1.0,1.0,1.0 ],
            "tick" : [self.player.cardtick+40.0],
            "texBuffer"            : PotionCard.textures[self.fridx//90],
            "translation_local"    : [ 0, 0 ],
            "scale_local"          : [ 0.7,0.7 ],
            "translation_world"    : [ -7.0,-3.2],
            "scale_world"          : [1.0,1.0],
            "view"                 : Hud.view,
            "rotation_local"       : 0.0,
            "filter_color"         : [1.0,1.0,1.0,1.0],
            "uv_translate"         : [ 0,0 ] }

class GunCard(Card):

    icons = BGL.assets.get("KT-player/animation/weapon_icons")
    spheres = BGL.assets.get("KT-player/animation/weapon_spheres")

    shader = BGL.assets.get("KT-player/shader/potion")

    def render(self):
        with BGL.blendmode.alpha_over:
            if(self.player.gun.slot2 is None):
                Card.primitive.render_shaded( GunCard.shader, self.get_shader_params(0) )
            else:
                Card.primitive.render_shaded( GunCard.shader, self.get_shader_params(0) )
                Card.primitive.render_shaded( GunCard.shader, self.get_shader_params(1) )

    def __init__(self, player):
        self.fridx = choice( range(0,180) )
        self.player = player

    def tick(self):
        self.fridx = (self.fridx + 1) %180

    def get_shader_params(self,right):
        if(self.player.gun.slot2 is None):
            return {
                "flashamt" : [ self.player.potionFlash ],
                "statusamt" : [ 1.0 ],
                "statuscolor" : [ 1.0,1.0,1.0,1.0 ],
                "tick" : [self.player.cardtick+40.0],
                "texBuffer"            : GunCard.icons[self.player.gun.slot1],
                "translation_local"    : [ 0, 0 ],
                "scale_local"          : [ 0.7,0.7 ],
                "translation_world"    : [ 7.0,-3.2],
                "scale_world"          : [1.0,1.0],
                "view"                 : Hud.view,
                "rotation_local"       : 0.0,
                "filter_color"         : [1.0,1.0,1.0,1.0],
                "uv_translate"         : [ 0,0 ] }
        else:
            if right==0:
                return {
                    "flashamt" : 0.0,
                    "statusamt" : [ 1.0 ],
                    "statuscolor" : [ 1.0,1.0,1.0,1.0 ],
                    "tick" : [self.player.cardtick+40.0],
                    "texBuffer"            : GunCard.icons[self.player.gun.slot1],
                    "translation_local"    : [ -0.9, 0.2 ],
                    "scale_local"          : [ 0.45,0.45 ],
                    "translation_world"    : [ 7.0,-3.4],
                    "scale_world"          : [1.0,1.0],
                    "view"                 : Hud.view,
                    "rotation_local"       : 0.0,
                    "filter_color"         : [1.0,1.0,1.0,1.0],
                    "uv_translate"         : [ 0,0 ] }
            return {
                "flashamt" : 0.0,
                "statusamt" : [ 1.0 ],
                "statuscolor" : [ 1.0,1.0,1.0,1.0 ],
                "tick" : [self.player.cardtick+40.0],
                "texBuffer"            : GunCard.icons[self.player.gun.slot2],
                "translation_local"    : [ 0.7, -0.3 ],
                "scale_local"          : [ 0.51,0.51 ],
                "translation_world"    : [ 7.0,-3.4],
                "scale_world"          : [1.0,1.0],
                "view"                 : Hud.view,
                "rotation_local"       : 0.0,
                "filter_color"         : [1.0,1.0,1.0,1.0],
                "uv_translate"         : [ 0,0 ] }
