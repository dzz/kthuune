from Beagle import API as BGL
from Beagle import Platform
from Newfoundland.Renderers.FloorRenderer import FloorRenderer
from Newfoundland.Renderers.LightMapper import LightMapper
from .uniform_fade import uniform_fade
from Newfoundland.Object import GuppyRenderer

class DFRenderer( FloorRenderer ):

    GR = GuppyRenderer()
    HittableShader = BGL.assets.get("KT-compositor/shader/hittables")

    def __init__(self,**kwargs):
        self.guppyRenderer = DFRenderer.GR
        FloorRenderer.__init__(self,**kwargs)

    def create_compositing_buffers(self):
        self.photon_buffer = BGL.framebuffer.from_screen()
        self.shadow_buffer = BGL.framebuffer.from_screen()
        self.floor_buffer = BGL.framebuffer.from_screen(filtered=True, scale = 1.0)
        self.light_buffer = BGL.framebuffer.from_screen(filtered=True, scale = 1.0)
        self.object_buffer = BGL.framebuffer.from_screen(filtered=True, scale = 1.0)
        self.canopy_buffer = BGL.framebuffer.from_screen(filtered=True, scale = 1.0)
        self.hittable_buffer = BGL.framebuffer.from_screen(filtered=True, scale = 0.5)

    def encode_player_lights( self ):
        return list(map(lambda player: { "position": player.p, "color" : [0.34,0.34,0.42,1.0], "radius" : player.sight_radius },self.get_player_objects()))

    def precompute_frame(self):
        """ Pre-render compositing """

        self.photon_map.compute_next()
        self.compute_vision_lightmap()
        self.compute_dynamic_lightmap()

        with BGL.context.render_target( self.shadow_buffer ):
            BGL.context.clear(1.0,1.0,1.0,1.0)
            with BGL.blendmode.alpha_over:
                self.render_objects("shadow")

        with BGL.context.render_target( self.floor_buffer ):
            BGL.context.clear(0.0,0.0,0.0,0.0)
            if( self.using_tilemap):
                self.render_tiles()
            with BGL.blendmode.alpha_over:
                self.render_objects("floor")

        #with BGL.context.render_target( self.photon_buffer ):
        #    BGL.context.clear(0.0,0.0,0.0,1.0)
        #    self.render_photon_map()

        with BGL.context.render_target( self.light_buffer ):
            if(self.player.dash_flash):
                with BGL.blendmode.alpha_over:
                    uniform_fade.apply_fadeout( 1.0 / 24.0 )
            else:
                BGL.context.clear(0.0,0.0,0.0,0.0)
            with BGL.blendmode.add:
                self.render_static_lightmap()
                self.dynamic_lightmap.get_lightmap_framebuffer().render_processed( FloorRenderer.pixel_copy_shader )

        with BGL.context.render_target( self.object_buffer ):

            if(self.player.dash_flash):
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
                    BGL.context.clear(0.0,0.0,0.0,0.0)
            with BGL.blendmode.alpha_over:
                self.render_objects("popup")


        with BGL.context.render_target( self.hittable_buffer ):
            with BGL.blendmode.alpha_over:
                uniform_fade.apply_fadeout( 1.0 / 32.0 )
                renderable_objects = self.player.hittable_hilight
                self.guppyRenderer.renderObjects( renderable_objects )
            
        #with BGL.context.render_target( self.canopy_buffer ):
        #    BGL.context.clear(0.0,0.0,0.0,0.0)
        #    with BGL.blendmode.alpha_over:
        #        self.render_objects("canopy")

    def render_objects(self, buftarget):
        """ Render floor objects """
        objects = []
        objects.extend( self.objects )
        objects.extend( self.get_player_objects() )
        renderable_objects = list(filter(lambda x: x.should_draw() and x.visible and x.buftarget == buftarget, objects))
        self.guppyRenderer.renderObjects( renderable_objects )

    def render_composite(self):
        shader  = self.compositor_shader
        with BGL.blendmode.alpha_over:
            BGL.compositor.render_composite( shader, {
                "tick"              : self._tick,
                "camera_position" : self.camera.p,
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
        with BGL.blendmode.alpha_over:
            self.render_objects("canopy")
        with BGL.blendmode.add:
            self.hittable_buffer.render_processed(DFRenderer.HittableShader, { "amt" : self.player.hittable_hint_real})

    def configure_vision_lightmapper(self):
        class FadingLightMapper( LightMapper ):
            def clear(self):
                with BGL.blendmode.alpha_over:
                    #BGL.context.clear(0.0,0.0,0.0,1.0)
                    uniform_fade.apply_fadeout( 0.4 )

        self.player_lights = []
        vision_lightmapper = FadingLightMapper( 
                lights = self.player_lights,
                geometry = self.get_occluders(), 
                camera = self.camera,
                width = self.vision_lightmap_width,
                height = self.vision_lightmap_height )

        print("RETURNING CUSTOM VISION MAPPER")
        return vision_lightmapper
