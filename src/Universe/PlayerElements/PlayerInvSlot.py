from Beagle import API as BGL
from Newfoundland.Object import Object
from .Hud import Hud
from math import floor

class PlayerInvSlot():
    _tick = 0.0
    offs = 0.8
    shader = BGL.assets.get("KT-player/shader/islot")
    primitive = BGL.primitive.unit_uv_square
    icons = {
        "hp_vial" : [ 
                        BGL.assets.get("KT-player/texture/healthvial0000"),
                        BGL.assets.get("KT-player/texture/healthvial0001")
                    ]
    }
    def tick():
        PlayerInvSlot._tick = PlayerInvSlot._tick + 0.01

    def render(idx, icon, selected, active):

        filter_color = [0.7,0.7,0.7,0.7]
        if(selected):
            filter_color = [1.0,1.0,1.0,1.0]
        PlayerInvSlot.primitive.render_shaded( PlayerInvSlot.shader, PlayerInvSlot.get_shader_params(idx, filter_color, active) )

        if icon and icon in PlayerInvSlot.icons:
            with BGL.blendmode.alpha_over:
                PlayerInvSlot.primitive.render_shaded( PlayerInvSlot.shader, PlayerInvSlot.get_icon_shader_params(idx, filter_color, icon, active) )
            

    def get_shader_params(idx, filter_color, active):

        yoffs = 0
        if(active):
            yoffs = 0.15
        return {
            "texBuffer"            : BGL.assets.get("KT-player/texture/inventory_slot"),
            "translation_local"    : [ 0, 0 ],
            "scale_local"          : [ 2.4*0.15,3.2*0.15 ],
            "translation_world"    : [ (-7.5) + (idx*PlayerInvSlot.offs),3.8 - yoffs],
            "scale_world"          : [1.0,1.0],
            "view"                 : Hud.view,
            "rotation_local"       : 0.0,
            "filter_color"         : filter_color,
            "uv_translate"         : [ 0,0 ] }

    def get_icon_shader_params(idx, filter_color, icon, active):
        yoffs = 0
        if(active):
            yoffs = 0.15
        return {
            "texBuffer"            : PlayerInvSlot.icons[icon][ (floor(PlayerInvSlot._tick)+idx)%len(PlayerInvSlot.icons[icon]) ],
            "translation_local"    : [ 0, 0 ],
            "scale_local"          : [ 0.4,0.4 ],
            "translation_world"    : [ (-7.5) + (idx*PlayerInvSlot.offs),3.8 - yoffs],
            "scale_world"          : [1.0,1.0],
            "view"                 : Hud.view,
            "rotation_local"       : 0.0,
            "filter_color"         : filter_color,
            "uv_translate"         : [ 0,0 ] }
