from Beagle import API as BGL

class ParallaxBackground:
    animate = {
        "city" : 0.0,   
        "lw" : 0.0,
        "ks" : 0.001,
    }
    shaders = {
        "city" : BGL.assets.get("KT-city/shader/city"),
        "lw" : BGL.assets.get("KT-lw/shader/lw"),
        "ks" : BGL.assets.get("KT-ks/shader/ks") }
    primitive = BGL.primitive.unit_uv_square
    layers = { "city" : [
        ( BGL.assets.get('KT-city/texture/city2_background'), 1.0 ),
        ( BGL.assets.get('KT-city/texture/city2_mountains_far'), 1.1 ),
        ( BGL.assets.get('KT-city/texture/city2_mountains_near'), 1.2 ),
        ( BGL.assets.get('KT-city/texture/city2_buildings_far'), 1.3 ),
        ( BGL.assets.get('KT-city/texture/city2_buildings_middle'), 1.4 ),
        ( BGL.assets.get('KT-city/texture/city2_buildings_near'), 1.5 ),
    ],
        "lw" : [

        ( BGL.assets.get('KT-lw/texture/lw_background'), 1.0 ),
        ( BGL.assets.get('KT-lw/texture/lw_mountains_far'), 1.1 ),
        ( BGL.assets.get('KT-lw/texture/lw_mountains_near'), 1.2 ),
        ( BGL.assets.get('KT-lw/texture/lw_buildings_far'), 1.3 ),
        ( BGL.assets.get('KT-lw/texture/lw_buildings_middle'), 1.4 ),
        ( BGL.assets.get('KT-lw/texture/lw_buildings_near'), 1.5 ),

        ],
        "ks" : [
        ( BGL.assets.get('KT-ks/texture/ks0'), 1.0 ),
        ( BGL.assets.get('KT-ks/texture/ks1'), 1.1 ),
        ( BGL.assets.get('KT-ks/texture/ks2'), 1.2 ),
        ( BGL.assets.get('KT-ks/texture/ks3'), 1.3 ),
        ( BGL.assets.get('KT-ks/texture/ks4'), 1.4 ),
        ( BGL.assets.get('KT-ks/texture/ks5'), 1.5 ),
        ( BGL.assets.get('KT-ks/texture/ks6'), 1.8 )
        ]
     }

    def render(x, skin = None, tick = 0.0 ):
        if not skin:
            skin = "lw"
        with BGL.blendmode.alpha_over:
            for layer in ParallaxBackground.layers[skin]:
                ParallaxBackground.primitive.render_shaded(ParallaxBackground.shaders[skin],  { "texBuffer" : layer[0], "offs": (x+(tick*ParallaxBackground.animate[skin]))*layer[1]*0.6 } )

