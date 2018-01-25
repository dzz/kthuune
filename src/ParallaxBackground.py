from Beagle import API as BGL

class ParallaxBackground:
    shader = BGL.assets.get("KT-city/shader/city")
    primitive = BGL.primitive.unit_uv_square
    layers = [
        ( BGL.assets.get('KT-city/texture/city2_background'), 1.0 ),
        ( BGL.assets.get('KT-city/texture/city2_mountains_far'), 1.1 ),
        ( BGL.assets.get('KT-city/texture/city2_mountains_near'), 1.2 ),
        ( BGL.assets.get('KT-city/texture/city2_buildings_far'), 1.3 ),
        ( BGL.assets.get('KT-city/texture/city2_buildings_middle'), 1.4 ),
        ( BGL.assets.get('KT-city/texture/city2_buildings_near'), 1.5 ),
    ]

    def render(x):
        with BGL.blendmode.alpha_over:
            for layer in ParallaxBackground.layers:
                ParallaxBackground.primitive.render_shaded(ParallaxBackground.shader,  { "texBuffer" : layer[0], "offs": x*layer[1] } )

