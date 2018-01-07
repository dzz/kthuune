from Beagle import API as BGL
from Beagle import Platform
from Newfoundland.Renderers.FloorRenderer import FloorRenderer
from Newfoundland.Renderers.LightMapper import LightMapper
from .uniform_fade import uniform_fade
from Newfoundland.Object import GuppyRenderer, Object
from random import sample

class DFRenderer( FloorRenderer ):
    photon_buffer = BGL.framebuffer.from_screen()
    shadow_buffer = BGL.framebuffer.from_screen()
    floor_buffer = BGL.framebuffer.from_screen(filtered=False, scale = 1.0)
    light_buffer = BGL.framebuffer.from_screen(filtered=True, scale = 1.0)
    object_buffer = BGL.framebuffer.from_screen(filtered=True, scale = 1.0)
    canopy_buffer = BGL.framebuffer.from_screen(filtered=True, scale = 1.0)
    hittable_buffer = BGL.framebuffer.from_screen(filtered=True, scale = 0.5)

    dynamic_lightmapper = None
    vision_lightmapper = None

    GR = GuppyRenderer()
    HittableShader = BGL.assets.get("KT-compositor/shader/hittables")
    canopy_shader = BGL.assets.get("KT-compositor/shader/canopy")

    def __init__(self,**kwargs):
        self.guppyRenderer = DFRenderer.GR
        DFRenderer.lbtick = 0
        FloorRenderer.__init__(self,**kwargs)

    #def configure_lightmaps(self):
    #    self.photon_map = None
    #    self.static_lightmap = self.compute_static_lightmap()
    #    self.static_lightmap.get_lightmap_texture().debugger_attach("static-lightmap")
    #    self.player_lights = []
    #    self.dynamic_lights = []

    #    if not DFRenderer.dynamic_lightmapper:
    #        DFRenderer.dynamic_lightmapper = self.configure_dynamic_lightmapper()

    #    self.dynamic_lightmap = DFRenderer.dynamic_lightmapper
    #    self.dynamic_lightmap.lights = self.dynamic_lights

    #    if not DFRenderer.vision_lightmapper:
    #        DFRenderer.vision_lightmapper = self.configure_vision_lightmapper()

    #    self.vision_lightmap = DFRenderer.vision_lightmapper
    #    self.vision_lightmap.lights = self.player_lights
            

    def create_compositing_buffers(self):
        self.photon_buffer = DFRenderer.photon_buffer
        self.shadow_buffer = DFRenderer.shadow_buffer
        self.floor_buffer = DFRenderer.floor_buffer
        self.light_buffer = DFRenderer.light_buffer
        self.object_buffer = DFRenderer.object_buffer
        self.canopy_buffer = DFRenderer.canopy_buffer
        self.hittable_buffer = DFRenderer.hittable_buffer

    def render(self):
        """ Perform final composite to active target """
        if(self.destroyed):
            print("trying to render a previously destroyed floor!!!")
            return
            
        self.precompute_frame()
        self.render_composite()

    max_lights = 100
    def visible_light(self,obj):
        if obj.mdist(self.player) < 200:
            return True
        else:
            return False

    def encode_light_objects(self, light_type):
        """ Converts Objects to LightMapper compatible lights if appropriate
        """
        baselights = list(map( lambda obj : { "position" : obj.p, "color" : obj.light_color, "radius" : obj.light_radius }, 
                         filter(lambda obj : obj.light_type == light_type and self.visible_light(obj), self.objects)))


        if light_type == Object.LightTypes.DYNAMIC_SHADOWCASTER and len(baselights)> DFRenderer.max_lights:
            return sample( baselights, DFRenderer.max_lights )
        return baselights


        
    def encode_player_lights( self ):
        return list(map(lambda player: { "position": player.p, "color" : [1.0,1.0,1.0,1.0], "radius" : player.sight_radius },self.get_player_objects()))

    def precompute_frame(self):
        """ Pre-render compositing """

        if(self.destroyed):
            print("Trying to render a destroyed floor!!!")
            return

        #self.vision_lightmap.clear()
        #self.vision_lightmap.white_out()

        if self.uses_vision:
            self.vision_lightmap.clear()
            self.compute_vision_lightmap()
            if self.active_vision_mute > 0.0:
                self.vision_lightmap.fade_out( self.active_vision_mute )
        else:
            self.vision_lightmap.white_out()

        #    if self.fade_vision_amt > 0.0:
        #        with BGL.context.render_target( self.vision_lightmap.target_buffer):
        #            with BGL.blendmode.alpha_over:
        #                uniform_fade.apply_fadeout( self.fade_vision_amt, [1.0,1.0,1.0] )
        #else:
        #    self.vision_lightmap.white_out()
        #        
        DFRenderer.lbtick +=1

        if(self.photon_map):
            self.photon_map.compute_next()
        #if(DFRenderer.lbtick%0==1):
        self.compute_dynamic_lightmap()

        with BGL.context.render_target( self.shadow_buffer ):
            BGL.context.clear(1.0,1.0,1.0,1.0)
            with BGL.blendmode.alpha_over:
                self.render_objects("shadow")
                self.tilemap_fg.render()

        with BGL.context.render_target( self.floor_buffer ):
            BGL.context.clear(0.0,0.0,0.0,0.0)
            with BGL.blendmode.alpha_over:
                self.render_objects("underfloor" )
            if( self.using_tilemap):
                    self.render_tiles()
            with BGL.blendmode.alpha_over:
                self.render_objects("floor" )

        #with BGL.context.render_target( self.photon_buffer ):
        #    BGL.context.clear(0.0,0.0,0.0,1.0)
        #    self.render_photon_map()

        with BGL.context.render_target( self.light_buffer ):
            if(self.player.dash_flash):
                with BGL.blendmode.alpha_over:
                    uniform_fade.apply_fadeout( 1.0 / 24.0 )
            else:
                uniform_fade.apply_fadeout( 1.0 / 48.0 )
            with BGL.blendmode.add:
                self.render_static_lightmap()
                self.dynamic_lightmap.get_lightmap_framebuffer().render_processed( FloorRenderer.pixel_copy_shader )

        with BGL.context.render_target( self.object_buffer ):

            self.blurring = True
            if(self.player.dash_flash) or self.player.slash.visible:
                with BGL.blendmode.alpha_over:
                    uniform_fade.apply_fadeout( 1.0 / 8.0 )
            elif (self.player.hp < 0.0):
                    with BGL.blendmode.alpha_over:
                        uniform_fade.apply_fadeout( 1.0 / 12.0 )
            elif (self.player.link_count > 0):
                    with BGL.blendmode.alpha_over:
                        uniform_fade.apply_fadeout( 1.0 / 16.0 )
            else:
                with BGL.blendmode.alpha_over:
                    self.blurring = False
                    BGL.context.clear(0.0,0.0,0.0,0.0)
            with BGL.blendmode.alpha_over:
                self.render_objects("popup")


        with BGL.context.render_target( self.hittable_buffer ):
            with BGL.blendmode.alpha_over:
                uniform_fade.apply_fadeout( 1.0 / 8.0 )
                renderable_objects = self.player.hittable_hilight
                self.guppyRenderer.renderObjects( renderable_objects )
                self.render_objects( "additive" )

            
        #with BGL.context.render_target( self.canopy_buffer ):
        #    BGL.context.clear(0.0,0.0,0.0,0.0)
        #    with BGL.blendmode.alpha_over:
        #        self.render_objects("canopy")

    def render_objects(self, buftarget, texture_priority = False):
        """ Render floor objects """
        objects = []
        objects.extend( self.objects )
        objects.extend( self.get_player_objects() )
        renderable_objects = list(filter(lambda x: x.should_draw() and x.visible and x.buftarget == buftarget, objects))

        if not texture_priority:
            self.guppyRenderer.renderObjects( renderable_objects )
        else:
            self.guppyRenderer.renderTexturePriorityObjects( renderable_objects )


    def render_canopy(self):
        with BGL.context.render_target( self.canopy_buffer):
            BGL.context.clear(1.0,1.0,1.0,0.0)
            with BGL.blendmode.alpha_over:
                self.render_objects("canopy", True)
        with BGL.blendmode.alpha_over:
            self.canopy_buffer.render_processed(DFRenderer.canopy_shader, { "light_buffer" : self.light_buffer })

    def render_preview(self):
        shader = BGL.assets.get("KT-compositor/shader/compositor")
        with BGL.blendmode.alpha_over:
            BGL.compositor.render_composite( shader, {
                "tick"              : self._tick,
                "camera_position" : self.camera.p,
                "fuzz_amt"  : self.fuzz_amt,
                "floor_buffer" : self.floor_buffer,
                "shadow_buffer" : self.shadow_buffer,
                "light_buffer" : self.light_buffer,
                "object_buffer" : self.object_buffer,
                "vision_buffer" : self.vision_lightmap.get_lightmap_texture(),
                "photon_buffer" : self.photon_buffer,
                "reflect_map" : self.reflection_map,
                "canopy_buffer" : self.canopy_buffer,
                "target_width" : Platform.video.get_screen_width(),
                "target_height" : Platform.video.get_screen_height() 
            })
        self.render_canopy()

    def render_composite(self):
        #print("FRAMESTART")
        shader  = self.compositor_shader
        with BGL.context.render_target( self.object_buffer ):
            with BGL.blendmode.add:
                self.hittable_buffer.render_processed(DFRenderer.HittableShader, { "amt" : self.player.hittable_hint_real})
        with BGL.blendmode.alpha_over:
            BGL.compositor.render_composite( shader, {
                "tick"              : self._tick,
                "camera_position" : self.camera.p,
                "fuzz_amt"  : self.fuzz_amt,
                "floor_buffer" : self.floor_buffer,
                "shadow_buffer" : self.shadow_buffer,
                "light_buffer" : self.light_buffer,
                "object_buffer" : self.object_buffer,
                "vision_buffer" : self.vision_lightmap.get_lightmap_texture(),
                "photon_buffer" : self.photon_buffer,
                "reflect_map" : self.reflection_map,
                "canopy_buffer" : self.canopy_buffer,
                "target_width" : Platform.video.get_screen_width(),
                "target_height" : Platform.video.get_screen_height() 
            })
        self.render_canopy()
        with BGL.blendmode.add:
            self.render_objects( "additive" )

    def configure_vision_lightmapper(self):
        class FadingLightMapper( LightMapper ):
            def clear(self):
                with BGL.context.render_target( self.target_buffer):
                    with BGL.blendmode.alpha_over:
                        #BGL.context.clear(0.0,0.0,0.0,1.0)
                        uniform_fade.apply_fadeout( 0.2, [0.0,0.0,0.0] )

            def fade_out(self,amt):
                with BGL.context.render_target( self.target_buffer):
                    with BGL.blendmode.alpha_over:
                        uniform_fade.apply_fadeout( amt, [1.0,1.0,1.0] )

        self.player_lights = []
        vision_lightmapper = FadingLightMapper( 
                lights = self.player_lights,
                geometry = self.get_occluders(), 
                camera = self.camera,
                width = self.vision_lightmap_width,
                height = self.vision_lightmap_height )

        print("RETURNING CUSTOM VISION MAPPER")
        return vision_lightmapper
