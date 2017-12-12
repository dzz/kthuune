from Beagle import API as BGL
from random import uniform
from .KSounds import KSounds
from .Renderers.uniform_fade import  uniform_fade
from math import sin


class Icon():
    primitive = BGL.primitive.unit_uv_square
    view = BGL.view.widescreen_16_9
    shader = BGL.assets.get("beagle-2d/shader/beagle-2d")

    def __init__(self):
        self.tlocal = [ 0.0,0.0]
    def get_shader_params(self):
        return {
            "texBuffer"            : self.texture,
            "translation_local"    : [0.0,-0.7],
            "scale_local"          : [ 2.5, 2.5 ],
            "translation_world"    : self.tlocal,
            "scale_world"          : [ 1.0,1.0],
            "view"                 : Icon.view,
            "rotation_local"       : 0.0,
            "filter_color"         : [ 1.0,1.0,1.0,1.0 ],
            "uv_translate"         : [ 0,0 ] }

    def render(self, dr):
        print(dr)
        sp = self.get_shader_params()
        sp['filter_color'] = [ dr*0.2,dr*0.2,dr*0.2,1.0]
        sp['scale_world'][0] *= 1.0 + ((1.0-dr)*5)
        sp['scale_world'][1] *= 1.0 + ((1.0-dr)*5)
        Icon.primitive.render_shaded( Icon.shader, sp )
        
    
class CloudBackground:

    fb = BGL.framebuffer.from_screen()
    shader = BGL.assets.get("KT-compositor/shader/cloud_background")
    animation = BGL.assets.get('KT-forest/animation/clouds_compressed')
    primitive = BGL.primitive.unit_uv_square

    malagor = BGL.assets.get('KT-forest/texture/icon1')
    yaomat = BGL.assets.get('KT-forest/texture/icon2')

    def __init__(self):

        self.tree_position = [ 16.0, -82 ]
        self.malagor = Icon();
        self.malagor.texture = CloudBackground.malagor
        self.malagor.tlocal = [ -5.0,0.0]
        self.yaomat = Icon();
        self.yaomat.texture = CloudBackground.yaomat
        self.yaomat.tlocal = [ 5.0,0.0]

        self.white_texture = BGL.framebuffer.from_dims(1,1)
        with BGL.context.render_target(self.white_texture):
            BGL.context.clear(1.0,1.0,1.0,1.0)

        self.fr0 = 0.0
        self.fr1 = 0.0
        self.camera = None
        self.lightning = 0.0

    def tick(self):

        if uniform(0.0,120.0)<1.0:
            self.lightning = uniform(12,24.0)
            KSounds.play(KSounds.atmozap1)
        if uniform(0.0,120.0)<1.0:
            KSounds.play(KSounds.atmozap2)
            self.lightning = uniform(-12,-24)
        self.fr0 += 0.14
        self.fr1 += 0.3

        self.lightning*=0.95

    def render(self,floor):


        d = (abs(floor.player.p[0] - self.tree_position[0]) + abs(floor.player.p[1] - self.tree_position[1]))/2.0

        dr = 50
        if d>dr:
            d = dr
        d /= dr
        d=d*d*d
        d = 1.0 - d

        floor.override_base_zoom = 0.2 * (0.5*(1.0+d))
            
        with BGL.context.render_target( CloudBackground.fb):
            with BGL.blendmode.alpha_over:
                uniform_fade.apply_fadeout( 0.3, [0.0,0.0,0.0] )
            lightning = self.lightning
            floor.fuzz_amt = 1.2+(lightning*(0.3/24.0))

            with BGL.blendmode.alpha_over:
                CloudBackground.primitive.render_shaded( CloudBackground.shader, {
                    "bg_texture" : CloudBackground.animation[ int(self.fr0) % len(CloudBackground.animation) ],
                    "camera_position" : self.camera.p,
                    "parallax" : 0.001,
                    "vision_tex" : self.white_texture,
                    "lightning" : lightning
                })
            with BGL.blendmode.add:
                CloudBackground.primitive.render_shaded( CloudBackground.shader, {
                    "bg_texture" : CloudBackground.animation[ int(self.fr1) % len(CloudBackground.animation) ],
                    "camera_position" : self.camera.p,
                    "parallax" : -0.002,
                    "vision_tex" : self.white_texture,
                    "lightning" : -1*lightning
                })

                self.yaomat.render(d)
                self.malagor.render(d)

        CloudBackground.fb.render_processed(BGL.assets.get('beagle-2d/shader/passthru'))

        

    
    

