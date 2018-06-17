from Beagle import API as BGL
from Newfoundland.Object import Object

class FakeCamera():
    def __init__(self):
        self.p = [-100.0,0.0]

class CinematicPlane(Object):
    primitive = BGL.primitive.unit_uv_square
    view = BGL.view.widescreen_16_9
    shader = BGL.assets.get("beagle-2d/shader/beagle-2d")

    def __init__(self,ticker = lambda : None, texture = None ):
        self.x = 0.0
        self.y = 0.0
        self.vx = 0.01
        self.filter_color = [ 1.0,1.0,1.0,1.0 ]
        self.base_filter = 1.0

        self.sx = 5.0
        self.sy = 5.0

        self.warping = False
        self.ticker = ticker
        self.texture = texture
        pass

    def get_shader_params(self):
        return {
            "texBuffer"            : self.texture,
            "translation_local"    : [ 0, 0 ],
            "scale_local"          : [ self.sx, self.sy ],
            "translation_world"    : [ self.x, self.y ],
            "scale_world"          : [ 1.0,1.0],
            "view"                 : CinematicPlane.view,
            "rotation_local"       : 0.0,
            "filter_color"         : self.filter_color,
            "uv_translate"         : [ 0,0 ] }

    def tick(self):
        self.ticker(self)
        pass
        #if(self.rx<0.0):
        #    self.rx += self.vx
        #    self.vx *= 1.04
        #else:
        #    self.base_filter *= 1.04

        #if(self.x>0.0):
        #    self.x = 0.0

        #self.x = (self.x*0.95) + (self.rx*0.05)

        #self.filter_color = [
        #    self.base_filter,
        #    self.base_filter,
        #    self.base_filter,
        #    1.0
        #]

        #if self.base_filter>25.8:
        #    self.sx *= 1.12
        #    self.sy *= 0.8
        #    self.warping = True


    def render(self):
        CinematicPlane.primitive.render_shaded( CinematicPlane.shader, self.get_shader_params() )

class IntroCinematic():

    def __init__(self):

        self.white_texture = BGL.framebuffer.from_dims(1,1)
        with BGL.context.render_target(self.white_texture):
            BGL.context.clear(1.0,1.0,1.0,1.0)
    
        self.frame = 0.0


        def get_plane_ticker(id):
            def default_ticker(self):
                pass
            return default_ticker
            pass

        def plane_initializer(id):

            def set_defaults(plane):
                pass

            def default_initializer(plane):
                set_defaults(plane)
                return plane
                pass
            return default_initializer
            pass

        planes = [
            BGL.assets.get('KT-forest/texture/EarthLayer-cloudbg'),
            BGL.assets.get('KT-forest/texture/EarthLayer-sealev'),
            BGL.assets.get('KT-forest/texture/EarthLayer-parallax_clouds'), 
            BGL.assets.get('KT-forest/texture/EarthLayer-mountains'), 
            BGL.assets.get('KT-forest/texture/EarthLayer-reflectmtn'), 
            BGL.assets.get('KT-forest/texture/EarthLayer-ter_distant'), 
            BGL.assets.get('KT-forest/texture/EarthLayer-parallax_clouds2'), 
            BGL.assets.get('KT-forest/texture/EarthLayer-ter3'), 
            BGL.assets.get('KT-forest/texture/EarthLayer-ter2'), 
            BGL.assets.get('KT-forest/texture/EarthLayer-ter1'), 
        ]

        self.cinematic_planes = []
        for id, plane in enumerate(planes):
            self.cinematic_planes.append(
                plane_initializer(id)(CinematicPlane( texture = plane, ticker = get_plane_ticker(id) ))
            )

        self.camera = FakeCamera()

    def tick(self):

        for plane in self.cinematic_planes: plane.tick()
        self.frame = self.frame + 1.0
        if self.frame < 47.0*5:
            return True
        return False

    def render(self):
        BGL.context.clear( 0.0,0.0,0.0,1.0);
        with BGL.blendmode.alpha_over:
            for plane in self.cinematic_planes: plane.render()


