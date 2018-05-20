from Beagle import API as BGL
from random import choice
from .Hud import Hud

class Bar():
    texbar1 = BGL.assets.get('KT-player/texture/bar1')
    texbar2 = BGL.assets.get('KT-player/texture/bar2')

class Card():
    shader = BGL.assets.get("KT-player/shader/card")
    primitive = BGL.primitive.unit_uv_square

    def render(self):
        Card.primitive.render_shaded( Card.shader, self.get_shader_params() )

class HeartCard(Card):
    textures = [
            BGL.assets.get('KT-player/texture/heartcard0000'),
            BGL.assets.get('KT-player/texture/heartcard0001')
        ]
    #primitive = BGL.primitive.unit_uv_square
    def __init__(self, player):
        self.fridx = choice( range(0,180) )
        self.player = player
        self.statusamt = self.compute_value()
        self.impulse = 0.0
        self.real_impulse = 0.0

    def compute_value(self):
        return self.player.hp / 100

    def tick(self): 
        self.impulse *= 0.99
        self.fridx = (self.fridx + 1) %180
        last_value = self.statusamt
        self.statusamt = self.compute_value()
        if(self.statusamt!=last_value):
            if(self.impulse<3.0):
                self.impulse += 1.0
        self.real_impulse = min( 1.0, self.impulse )
        

    def get_shader_params(self):

        return {
            "statusamt" : [ self.player.hp / 100.0 ],
            "statuscolor" : [ 1.0,0.0,0.0,1.0 ],
            "tick" : [ self.player.cardtick ],
            "impulse" : self.real_impulse,
            "texBuffer"            : Bar.texbar1,
            "translation_local"    : [ 0, 0 ],
            "scale_local"          : [ 4.0,1.0],
            "translation_world"    : [ 0.0,4.0 ],
            "scale_world"          : [1.0,1.0],
            "view"                 : Hud.view,
            "rotation_local"       : (self.real_impulse-0.5)*0.1,
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
        self.player = player
        self.statusamt = self.compute_value()
        self.impulse = 0.0
        self.real_impulse = 0.0

    def compute_value(self):
        return self.player.run_stamina / 100.0

    def tick(self):
        self.impulse *= 0.99
        self.fridx = (self.fridx + 1) %180
        last_value = self.statusamt
        self.statusamt = self.compute_value()
        if(self.statusamt!=last_value):
            if(self.impulse<3.0):
                self.impulse += 1.0
        self.real_impulse = min( 1.0, self.impulse )

    def get_shader_params(self):
        return {
            "statusamt" : [ self.statusamt ],
            "statuscolor" : [ 0.0,1.0,0.0,1.0 ],
            "tick" : [self.player.cardtick+10.0],
            "impulse" : self.real_impulse,
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

class TelekineCard(Card):
    shader = BGL.assets.get("KT-player/shader/telekine")
    textures = [
            BGL.assets.get('KT-player/texture/birdman0000'),
            BGL.assets.get('KT-player/texture/birdman0001'),
            BGL.assets.get('KT-player/texture/birdman0002'),
            BGL.assets.get('KT-player/texture/birdman0001')
        ]

    def render(self):
        with BGL.blendmode.alpha_over:
            Card.primitive.render_shaded( TelekineCard.shader, self.get_shader_params() )

    def __init__(self, player):
        self.fridx = choice( range(0,360) )
        self.player = player

    def tick(self):
        self.fridx = (self.fridx + 1) %360

    def get_shader_params(self):
        return {
            "flashamt" : [ self.player.telekineFlash ],
            "statusamt" : [ self.player.teleportAmt / 100.0 ],
            "statuscolor" : [ 1.0,1.0,1.0,1.0 ],
            "tick" : [self.player.cardtick+40.0],
            "texBuffer"            : TelekineCard.textures[self.fridx//90],
            "translation_local"    : [ 0, 0 ],
            "scale_local"          : [ 0.7,0.7 ],
            "translation_world"    : [ -7.0,3.2],
            "scale_world"          : [1.0,1.0],
            "view"                 : Hud.view,
            "rotation_local"       : 0.0,
            "filter_color"         : [1.0,1.0,1.0,1.0],
            "uv_translate"         : [ 0,0 ] }

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
