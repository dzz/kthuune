from Beagle import API as BGL

from .Hud import Hud

class Cooldown:
    primitive = BGL.primitive.unit_uv_square
    shader = BGL.assets.get("beagle-2d/shader/beagle-2d")
    t = 0

    sword_amt = 0.0
    tele_amt = 0.0

    def tick(player):

        sword_impulse = 0.0
        if(player.throw_sword_attack.cooldown == 0):
            sword_impulse = 1.0
        else:
            Cooldown.sword_amt = 0.0

        Cooldown.sword_amt = (Cooldown.sword_amt*0.8) + (sword_impulse*0.2)

        tele_impulse = 0.0
        if(player.snap_cooldown <= 0):
            tele_impulse = 1.0
        else:
            Cooldown.tele_amt = 0.0

        Cooldown.tele_amt = (Cooldown.tele_amt*0.8) + (tele_impulse*0.2)
        
        Cooldown.t += 1
        if(Cooldown.t == 32):
            Cooldown.t = 0

class SwordCooldown:
    textures = [
            BGL.assets.get('KT-player/texture/swordcard0000'),
            BGL.assets.get('KT-player/texture/swordcard0001')
        ]
    def render():
        Cooldown.primitive.render_shaded(Cooldown.shader, {
            "texBuffer" : SwordCooldown.textures[Cooldown.t//16],
            "translation_local" : [ 0.0, 0.0 ],
            "scale_local" : [ 0.5, 0.75 ],
            "translation_world" : [ 7.0, 3.5 ],
            "scale_world" : [ 1.0, 1.0 ],
            "view" : Hud.view,
            "rotation_local" : 0.0,
            "filter_color" : [ 0.0,1.0,0.0,Cooldown.sword_amt],
            "uv_translate" : [ 0,0 ]
        })

class TelekineCooldown:
    textures = [
            BGL.assets.get('KT-player/texture/warpcard0000'),
            BGL.assets.get('KT-player/texture/warpcard0001')
        ]
    def render():
        Cooldown.primitive.render_shaded(Cooldown.shader, {
            "texBuffer" : TelekineCooldown.textures[Cooldown.t//16],
            "translation_local" : [ 0.0, 0.0 ],
            "scale_local" : [ 0.5, 0.75 ],
            "translation_world" : [ -7.0, 3.5 ],
            "scale_world" : [ 1.0, 1.0 ],
            "view" : Hud.view,
            "rotation_local" : 0.0,
            "filter_color" : [ 0.0,0.0,1.0,Cooldown.tele_amt],
            "uv_translate" : [ 0,0 ]
        })
        pass

