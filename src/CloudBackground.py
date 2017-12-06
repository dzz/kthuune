from Beagle import API as BGL

class CloudBackground:
    shader = BGL.assets.get("KT-compositor/shader/cloud_background")
    animation = BGL.assets.get('KT-forest/animation/clouds_compressed')
    primitive = BGL.primitive.unit_uv_square

    def __init__(self):
        self.white_texture = BGL.framebuffer.from_dims(1,1)
        with BGL.context.render_target(self.white_texture):
            BGL.context.clear(1.0,1.0,1.0,1.0)

        self.fr0 = 0.0
        self.fr1 = 0.0
        self.camera = None

    def tick(self):
        self.fr0 += 0.14
        self.fr1 += 0.3

    def render(self,floor):
        CloudBackground.primitive.render_shaded( CloudBackground.shader, {
            "bg_texture" : CloudBackground.animation[ int(self.fr0) % len(CloudBackground.animation) ],
            "camera_position" : self.camera.p,
            "parallax" : 0.001,
            "vision_tex" : self.white_texture
        })
        with BGL.blendmode.add:
            CloudBackground.primitive.render_shaded( CloudBackground.shader, {
                "bg_texture" : CloudBackground.animation[ int(self.fr1) % len(CloudBackground.animation) ],
                "camera_position" : self.camera.p,
                "parallax" : -0.002,
                "vision_tex" : self.white_texture
            })

    
    

