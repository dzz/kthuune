from Beagle import API as BGL
from Newfoundland.Object import Object
from random import uniform
from math import sin,cos
from .TitleCard import TitleCard
from ..CloudBackground import CloudBackground

FADEOUT_START = 2220 
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
        self.filter_color = [ 1.0,1.0,1.0,1.0 ]
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
        self.cloud_fade = 1.0


        #################

        PAR_CLOUDS = 2
        PAR_MTNS = 3
        PAR_REFLCT_MTNS = 4
        PAR_CLOUDS2 = 6
        PAR_TERDST = 5

        PAR_TER_FAR = 7
        PAR_TER_MID = 8
        PAR_TER_NEAR = 9
        PAR_TER_NEAREST = 10

        #FOREGROUND_FG = 

        owner = self
        def get_plane_ticker(id):
            def default_ticker(plane):

                plane._t += 0.1
                fadein = float( 0.048 / float((id*2)+1) )
                if(owner.frame<1600) and (owner.frame>200): 
                    for i in range (0,4): 
                        val = min(1.0,plane.filter_color[i] + (fadein/float(i+1)))
                        plane.filter_color[i] = val
                if(owner.frame>FADEOUT_START): 
                    for i in range (0,4): 
                        val = max(0.0,plane.filter_color[i] - (fadein/float(i+1)))
                        plane.filter_color[i] = val
                else:
                    owner.cloud_background.lightning = 0.0


                if id == 0:
                    plane.sx *= 1.0003
                if id == PAR_CLOUDS:
                    plane.x -= 0.004
                    plane.y = sin(plane._t*0.08)*0.04
                    plane.sx *= 1.00005
                if id == PAR_CLOUDS2:
                    plane.x -= 0.002
                    plane.y = cos(plane._t*0.04)*0.06
                    plane.sx *= 1.00004

                if id == PAR_MTNS:
                    plane.x -= 0.0008
                if id == PAR_REFLCT_MTNS:
                    plane.x -= 0.0008
                if id == PAR_TERDST:
                    plane.x -= 0.0012

                if id == PAR_TER_FAR:
                    plane.x -= 0.002
                    plane.y = sin(plane._t*0.1)*0.03
                if id == PAR_TER_MID:
                    plane.x -= 0.0043
                    plane.y = cos(plane._t*0.2)*0.02
                if id == PAR_TER_NEAR:
                    plane.x -= 0.0064
                if id == PAR_TER_NEAREST:
                    plane.x -= 0.0110

                plane.x -= 0.008

            return default_ticker

        def plane_initializer(id):
            def set_defaults(plane):

                plane._t = uniform(0.0,6.3)

                plane.x += 5.0
                plane.sx = 15.0
                plane.sy = 3.0
                plane.filter_color = [ 0.0,0.0,0.0,1.0 ]

                if id in [ PAR_CLOUDS, PAR_CLOUDS2 ]:
                    plane.x += 35.0

                if id == PAR_MTNS:
                    plane.x += 8.0

                if id == PAR_TERDST:
                    plane.x += 11.0

                if id == PAR_TER_FAR:
                    plane.x += 8.0
                    plane.sx *= 0.98
                    plane.sy *= 0.98
                if id == PAR_TER_MID:
                    plane.x += 15.0
                if id == PAR_TER_NEAR:
                    plane.x += 23.0
                if id == PAR_TER_NEAREST:
                    plane.x += 35.0
                    plane.sx *= 1.02
                    plane.sy *= 1.02
                if not id in [ 0, PAR_MTNS ]:
                    plane.x -= 10

            def default_initializer(plane):
                set_defaults(plane)
                return plane
            return default_initializer

        ################

        planes = [
            (BGL.assets.get('KT-forest/texture/EarthLayer-cloudbg'), BGL.blendmode.alpha_over  ),
            (BGL.assets.get('KT-forest/texture/EarthLayer-sealev'), BGL.blendmode.alpha_over ),
            (BGL.assets.get('KT-forest/texture/EarthLayer-parallax_clouds'), BGL.blendmode.add ),
            (BGL.assets.get('KT-forest/texture/EarthLayer-mountains'), BGL.blendmode.alpha_over ),
            (BGL.assets.get('KT-forest/texture/EarthLayer-reflectmtn'), BGL.blendmode.alpha_over ),
            (BGL.assets.get('KT-forest/texture/EarthLayer-ter_distant'), BGL.blendmode.alpha_over ),
            (BGL.assets.get('KT-forest/texture/EarthLayer-parallax_clouds2'), BGL.blendmode.alpha_over ),
            (BGL.assets.get('KT-forest/texture/EarthLayer-ter3'), BGL.blendmode.alpha_over ),
            (BGL.assets.get('KT-forest/texture/EarthLayer-ter2'), BGL.blendmode.alpha_over ),
            (BGL.assets.get('KT-forest/texture/EarthLayer-ter1'), BGL.blendmode.alpha_over ),
            (BGL.assets.get('KT-forest/texture/EarthLayer-ter0'), BGL.blendmode.alpha_over )
        ]

        self.cinematic_planes = []
        for id, plane in enumerate(planes):
            self.cinematic_planes.append(
                plane_initializer(id)(CinematicPlane( texture = plane[0], blendmode = plane[1], ticker = get_plane_ticker(id) ))
            )

        self.camera = FakeCamera()
        self.title_card = TitleCard();
        self.title_card.reset("4199 A.D.")
        self.cloud_background = CloudBackground()
        self.cloud_background.camera = self.camera

    def tick(self):
        if( self.frame > FADEOUT_START ):
            self.cloud_background.tick()
            self.cloud_background.lightning *= self.cloud_fade
            self.cloud_fade *= 0.998
        self.title_card.tick()
        for plane in self.cinematic_planes: plane.tick()
        self.frame = self.frame + 1.0

        if( self.frame == 350):
            self.title_card.reset("COMPUTATION reigns supreme,",False)
        if( self.frame == 720):
            self.title_card.reset("HUMANITY rendered irrelevant.",False)
        if( self.frame == 1150):
            self.title_card.reset("CASIO CAIN destroyed the world",False)
        if( self.frame == 1600):
            self.title_card.reset("A world reclaimed by DEEP SOVEREIGN",False)
        if( self.frame == 2100):
            self.title_card.reset("NEW ERAS create NEW CHALLENGES",False)
        if( self.frame == 2520):
            self.title_card.reset("NEW kinds of VIRUSES...",False)

        ## The Infection is Spreading 

        
            
            
        self.camera.p[0] -= 0.01

        if self.frame < 2850:
            return True
        else:
            self.game.trigger_cinematic("beard")
            return True
        return False

    def render(self):
        BGL.context.clear( 0.0,0.0,0.0,1.0);
        if( self.frame > FADEOUT_START ):
            self.cloud_background.render()
        for plane in self.cinematic_planes:
            with plane.blendmode:
                plane.render()
        with BGL.blendmode.alpha_over:
            self.title_card.render()


