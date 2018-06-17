from Beagle import API as BGL
from Newfoundland.Object import Object
from ..Background import Background

class FakeCamera():
    def __init__(self):
        self.p = [-100.0,0.0]

class CinematicShip(Object):
    primitive = BGL.primitive.unit_uv_square
    texture = BGL.assets.get('KT-player/texture/ship_exterior')
    view = BGL.view.widescreen_16_9
    shader = BGL.assets.get("beagle-2d/shader/beagle-2d")

    def __init__(self):
        self.rx = -16.0
        self.x = self.rx
        self.vx = 0.01
        self.filter_color = [ 1.0,1.0,1.0,1.0 ]
        self.base_filter = 1.0

        self.sx = 5.0
        self.sy = 5.0

        self.warping = False
        pass

    def get_shader_params(self):
        return {
            "texBuffer"            : CinematicShip.texture,
            "translation_local"    : [ 0, 0 ],
            "scale_local"          : [ self.sx, self.sy ],
            "translation_world"    : [ self.x, 0.0 ],
            "scale_world"          : [ 1.0,1.0],
            "view"                 : CinematicShip.view,
            "rotation_local"       : 0.0,
            "filter_color"         : self.filter_color,
            "uv_translate"         : [ 0,0 ] }

    def tick(self):
        if(self.rx<0.0):
            self.rx += self.vx
            self.vx *= 1.04
        else:
            self.base_filter *= 1.04

        if(self.x>0.0):
            self.x = 0.0

        self.x = (self.x*0.95) + (self.rx*0.05)

        self.filter_color = [
            self.base_filter,
            self.base_filter,
            self.base_filter,
            1.0
        ]

        if self.base_filter>25.8:
            self.sx *= 1.12
            self.sy *= 0.8
            self.warping = True


    def render(self):
        CinematicShip.primitive.render_shaded( CinematicShip.shader, self.get_shader_params() )

class WarpCinematic():
    def __init__(self):

        self.white_texture = BGL.framebuffer.from_dims(1,1)
        with BGL.context.render_target(self.white_texture):
            BGL.context.clear(1.0,1.0,1.0,1.0)
    
        self.frame = 0.0
        self.ship = CinematicShip()
        self.camera = FakeCamera()
        self.background = Background()
        self.background.sky_texture = BGL.assets.get("KT-forest/texture/starfield1")
        self.background.bg_texture = BGL.assets.get("KT-forest/texture/nebula")
        self.background.camera = self.camera
        self.background.add_blending = True
        self.camera_vx = 0.2

    def tick(self):

        self.camera_vx *= 1.02
        if( self.ship.warping):
            self.camera_vx *= 1.01
        self.camera.p[0] += self.camera_vx

        self.ship.tick()
        self.frame = self.frame + 1.0
        if self.frame < 47.0*5:
            return True
        return False

    def render(self):
        BGL.context.clear( 0.0,0.0,0.0,1.0);
        self.background.render(self.white_texture)

        with BGL.blendmode.alpha_over:
            self.ship.render()


