from Beagle import API as BGL
from Newfoundland.Object import Object
from random import uniform
from math import sin,cos
from .TitleCard import TitleCard
from ..CloudBackground import CloudBackground

FADEOUT_START = 500 
class FakeCamera():
    def __init__(self):
        self.p = [-100.0,0.0]

class CinematicPlane(Object):
    primitive = BGL.primitive.unit_uv_square
    view = BGL.view.widescreen_16_9
    shader = BGL.assets.get("beagle-2d/shader/beagle-2d")

    def __init__(self,ticker = lambda : None, texture = None, blendmode = None ):
        self.x = 0.0
        self.y = 0.0
        self.vx = 0.01
        self.filter_color = [ 0.0,0.0,0.0,0.0 ]
        self.base_filter = 1.0

        self.sx = 5.0
        self.sy = 5.0

        self.warping = False
        self.ticker = ticker
        self.texture = texture
        self.blendmode = blendmode

    def get_shader_params(self):
        return {
            "texBuffer"            : self.texture,
            "translation_local"    : [ 0, 0 ],
            "scale_local"          : [ self.sx, self.sy ],
            "translation_world"    : [ self.x, self.y ],
            "scale_world"          : [ 0.8,0.8 ],
            "view"                 : CinematicPlane.view,
            "rotation_local"       : 0.0,
            "filter_color"         : self.filter_color,
            "uv_translate"         : [ 0,0 ] }

    def tick(self):
        self.ticker(self)
        pass

    def render(self):
        CinematicPlane.primitive.render_shaded( CinematicPlane.shader, self.get_shader_params() )

class BeardCinematic():

    def __init__(self):

        self.white_texture = BGL.framebuffer.from_dims(1,1)
        with BGL.context.render_target(self.white_texture):
            BGL.context.clear(1.0,1.0,1.0,1.0)
    
        self.frame = 0.0
        owner = self
        def get_plane_ticker(id):
            def default_ticker(plane):
                plane._t += 0.07
                fadein = float( 0.15 / float((id)+1) )
                if(owner.frame<1600) and (owner.frame>0): 
                    for i in range (0,4): 
                        val = min(1.0,plane.filter_color[i] + (fadein/float(i+1)))
                        plane.filter_color[i] = val
                if(owner.frame>FADEOUT_START): 
                    for i in range (0,4): 
                        val = max(0.0,plane.filter_color[i] - (fadein/float(i+1)))
                        plane.filter_color[i] = val

                spd = 0.7
                if id == 0:
                    plane.y -= (0.01)*spd
                if id == 1:
                    plane.y -= (0.013)*spd
                if id == 2:
                    plane.y -= (0.014)*spd
                if id == 3:
                    plane.y -= (0.016)*spd
                if id == 4:
                    plane.y -= (0.0135)*spd
                if id == 5:
                    plane.y -= (0.019)*spd
                if id == 6:
                    plane.y -= (0.022)*spd


            return default_ticker

        def plane_initializer(id):
            def set_defaults(plane):
                plane._t = uniform(0.0,6.3)

                plane.sx = 2.4
                plane.sy = 18.0
                plane.x += 5.0

                plane.y += 12.0
                if id == 6:
                    plane.y += 6.0
                if id == 4:
                    plane.y -= 6.0

            def default_initializer(plane):
                set_defaults(plane)
                return plane
            return default_initializer

        ################

        planes = [
            (BGL.assets.get('KT-forest/texture/GB-00_bg'), BGL.blendmode.alpha_over  ),
            (BGL.assets.get('KT-forest/texture/GB-01_light1'), BGL.blendmode.alpha_over  ),
            (BGL.assets.get('KT-forest/texture/GB-02_light2'), BGL.blendmode.add  ),
            (BGL.assets.get('KT-forest/texture/GB-03_beard0shadow'), BGL.blendmode.alpha_over  ),
            (BGL.assets.get('KT-forest/texture/GB-03_beard1'), BGL.blendmode.alpha_over  ),
            (BGL.assets.get('KT-forest/texture/GB-03_beard2'), BGL.blendmode.alpha_over  ),
            (BGL.assets.get('KT-forest/texture/GB-03_beard3'), BGL.blendmode.alpha_over  )
        ]

        self.cinematic_planes = []
        for id, plane in enumerate(planes):
            self.cinematic_planes.append(
                plane_initializer(id)(CinematicPlane( texture = plane[0], blendmode = plane[1], ticker = get_plane_ticker(id) ))
            )

        self.camera = FakeCamera()
        self.title_card = TitleCard();
        self.title_card.reset("The GREYBEARDS protect DEEP SOVEREIGN", False)
        self.title_card.centerx = 16
        self.title_card.top = 32

    def tick(self):
        self.title_card.tick()
        for plane in self.cinematic_planes: plane.tick()
        self.frame = self.frame + 1.0

        if( self.frame == 350):
            self.title_card.top = 64
            self.title_card.reset("They created the LORD series",False)
        if( self.frame == 810):
            self.title_card.top = 160
            self.title_card.reset("A new type of anti-virus...",False)
        if( self.frame == 1050):
            self.title_card.top = 192
            self.title_card.reset("innoculated with HUMANITY",False)

        ## The Infection is Spreading 

        #self.camera.p[0] -= 0.01

        if self.frame < 2850:
            return True
        return False

    def render(self):
        BGL.context.clear( 0.0,0.0,0.0,1.0);
        for plane in self.cinematic_planes:
            with plane.blendmode:
                plane.render()
        with BGL.blendmode.alpha_over:
            self.title_card.render()


