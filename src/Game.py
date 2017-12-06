import gc
from random import uniform, choice
from Beagle import API as BGL
from Newfoundland.Camera import Camera
from Newfoundland.Controllers import Controllers
from Newfoundland.Player import Player
from Newfoundland.BaseGame import BaseGame

from .DungeonFloor import DungeonFloor
from .DungeonCamera import DungeonCamera
from .KPlayer import KPlayer
from .KTState import KTState

from .superstructure import generate_qualified_areas
from .Generators.AreaLoader import get_area_data
from .Generators.ForestGraveyard import ForestGraveyard
from .GeneratorOptions import GeneratorOptions

from .Background import Background
from .CloudBackground import CloudBackground
from .Fog import Fog

from .Abilities import Abilities
from .Renderers.uniform_fade import uniform_fade 

import audio
class Game( BaseGame ):

    god_buffer = BGL.framebuffer.from_screen()
    god_shader = BGL.assets.get("KT-compositor/shader/god")

    paused = False
    area_name = None
    ###############

    def trigger_cinematic(self,key):
        from .WarpCinematic import WarpCinematic
        if key == "warp":
            self.active_cinematic = WarpCinematic()
            self.active_cinematic.game = self
        pass

    def build_area_test(self):
        area_raw = BGL.assets.get("KT-forest/textfile/area_test")
        area_def = get_area_data( area_raw )

        floor = DungeonFloor( tilescale =2, width = area_def["width"]*2, height = area_def["height"]*2, camera = self.camera, player = self.player, objects = [], area_def = area_def )
        floor.game = self
        return floor

    def build_area_tower(self):
        area_raw = BGL.assets.get("KT-forest/textfile/tower")
        area_def = get_area_data( area_raw )

        floor = DungeonFloor( tilescale =2, width = area_def["width"]*2, height = area_def["height"]*2, camera = self.camera, player = self.player, objects = [], area_def = area_def )
        floor.game = self
        return floor

    def build_area_doortest(self):
        area_raw = BGL.assets.get("KT-forest/textfile/doortest")
        area_def = get_area_data( area_raw )

        floor = DungeonFloor( music=BGL.assets.get('KT-player/path/polydrone'),

        god_shader = BGL.assets.get("KT-compositor/shader/ship_god"),
tilescale =2, width = area_def["width"]*2, height = area_def["height"]*2, camera = self.camera, player = self.player, objects = [], area_def = area_def )
        floor.game = self
        return floor

    def build_area_arena(self):
        area_raw = BGL.assets.get("KT-forest/textfile/arena")
        area_def = get_area_data( area_raw )

        floor = DungeonFloor( tilescale =2, width = area_def["width"]*2, height = area_def["height"]*2, camera = self.camera, player = self.player, objects = [], area_def = area_def )
        floor.game = self
        return floor

    def build_area_docks(self):
        area_raw = BGL.assets.get("KT-forest/textfile/docks")
        area_def = get_area_data( area_raw )

        floor = DungeonFloor( tilescale =2,
        god_shader = BGL.assets.get("KT-compositor/shader/ship_god"),

         width = area_def["width"]*2, height = area_def["height"]*2, camera = self.camera, player = self.player, objects = [], area_def = area_def )
        floor.using_tilemap = False
        floor.game = self
        return floor

    def build_area_oort_cloud(self):

        GeneratorOptions.TreeTopTextures = [
            BGL.assets.get("KT-forest/texture/crystal_1"),
            BGL.assets.get("KT-forest/texture/crystal_2"),
            BGL.assets.get("KT-forest/texture/crystal_3"),
            BGL.assets.get("KT-forest/texture/crystal_4")
        ]

        GeneratorOptions.TreeShadowTextures = GeneratorOptions.TreeTopTextures

        area_raw = BGL.assets.get("KT-forest/textfile/oort_cloud")
        area_def = get_area_data( area_raw )

        floor = DungeonFloor( 
        title = "The Oort Cloud",
        god_shader = BGL.assets.get("KT-compositor/shader/oort_god"),
        fog_level_base=0.5, tilescale =2, width = area_def["width"]*2, height = area_def["height"]*2, camera = self.camera, player = self.player, objects = [], area_def = area_def )
        floor.game = self
        return floor

    def build_area_crystals1(self):

        GeneratorOptions.TreeTopTextures = [
            BGL.assets.get("KT-forest/texture/crystal_1"),
            BGL.assets.get("KT-forest/texture/crystal_2"),
            BGL.assets.get("KT-forest/texture/crystal_3"),
            BGL.assets.get("KT-forest/texture/crystal_4")
        ]

        GeneratorOptions.TreeShadowTextures = GeneratorOptions.TreeTopTextures

        area_raw = BGL.assets.get("KT-forest/textfile/crystals1")
        area_def = get_area_data( area_raw )

        floor = DungeonFloor( 
        title = "Crystaline Structure I.",
        god_shader = BGL.assets.get("KT-compositor/shader/ship"),
        fog_level_base=0.5, tilescale =2, width = area_def["width"]*2, height = area_def["height"]*2, camera = self.camera, player = self.player, objects = [], area_def = area_def )
        floor.game = self
        floor.music = BGL.assets.get("KT-player/path/lacuna_canal")

        floor.vision_mute = 0.7
        floor.bg_texture = BGL.assets.get("KT-forest/texture/lightmap")
        floor.sky_texture = BGL.assets.get("KT-forest/texture/background")
        floor.parallax_sky = 0.005
        floor.parallax_bg = 0.01

        return floor

    def build_area_ship_type(self, key):
        # a generic level template with good settings for smaller areas without a lot of lighting requirements 
        GeneratorOptions.TreeTopTextures = [
            BGL.assets.get("KT-forest/texture/crystal_1"),
            BGL.assets.get("KT-forest/texture/crystal_2"),
            BGL.assets.get("KT-forest/texture/crystal_3"),
            BGL.assets.get("KT-forest/texture/crystal_4")
        ]

        GeneratorOptions.TreeShadowTextures = GeneratorOptions.TreeTopTextures

        area_raw = BGL.assets.get("KT-forest/textfile/"+key)
        area_def = get_area_data( area_raw )

        floor = DungeonFloor( 
            music = BGL.assets.get("KT-player/path/ship_music"),
            title = "The Xeoliex",
            god_shader = BGL.assets.get("KT-compositor/shader/ship_god"),
            fuzz_amt = 0.8,
            fog_level_base=0.5, 
            tilescale =2, 
            uses_vision=True, 
            fade_vision_amt=0.62, 
            width = area_def["width"]*2, 
            height = area_def["height"]*2, 
            camera = self.camera, 
            player = self.player, 
            objects = [], 
            area_def = area_def, 
            vision_mute = 0.7,
            renderer_config = { 
                "vision_lightmap_width" : 960,
                "vision_lightmap_height" : 540,
                "photon_map_width" : 1024,
                "photon_map_height" : 1024,
                "static_lightmap_width" : 1024,
                "static_lightmap_height" : 1024,
                "dynamic_lightmap_width" : 960,
                "dynamic_lightmap_height" : 540,
                "photon_mapper_config" : {
                    'stream' : True,
                    'photon_radius' :70.0,
                    'photon_emitter_power' : 0.01,
                    'photon_decay' : 0.9,
                    'photon_decay_jitter' : 0.4,
                    'photon_max_bounces' : 9,
                    'num_photons' : 8,
                    'photon_observe_chance' : 0.8
                },
                }
            )

        floor.game = self
        return floor

    def build_area_ship(self):
        return self.build_area_ship_type("ship")

    def build_area_lacuna_canal(self):
        floor = self.build_area_ship_type("lacuna_canal")
        floor.title = "Unknown Origins"
        floor.uses_vision = True

        floor.music = BGL.assets.get("KT-player/path/lacuna_canal")
        floor.sky_texture = BGL.assets.get("KT-forest/texture/starfield1")
        floor.bg_texture = BGL.assets.get("KT-forest/texture/nebula")
        floor.bg_mode = "add"
        floor.parallax_sky = 0.01
        floor.parallax_bg = 0.04
        floor.fog_level_base = 0.1
        floor.fuzz_amt = 0.3
        floor.vision_mute = 0.6
        return floor

    def build_area_chase(self):
        floor = self.build_area_ship_type("chase")
        floor.title = "..."
        floor.uses_vision = True

        floor.music = None
        floor.sky_texture = BGL.assets.get("KT-forest/texture/electrotrash")
        floor.bg_texture = BGL.assets.get("KT-forest/texture/electrofore")
        floor.parallax_sky = 0.01
        floor.parallax_bg = 0.04
        floor.fog_level_base = 1.0 #investigate

        floor.uses_vision = True
        return floor

    def build_area_platform(self):
        floor = self.build_area_ship_type("platform")
        floor.title = "..."
        floor.uses_vision = True

        floor.music = None
        floor.sky_texture = BGL.assets.get("KT-forest/texture/starfield1")
        floor.bg_texture = BGL.assets.get("KT-forest/texture/nebula")
        floor.parallax_sky = 0.01
        floor.parallax_bg = 0.04
        floor.fog_level_base = 1.0

        floor.uses_vision = True
        floor.god_shader = BGL.assets.get("KT-compositor/shader/oort_god")
        return floor

    def build_area_kiln(self):
        floor = self.build_area_ship_type("kiln")
        floor.title = "The Kiln"
        floor.uses_vision = False
        floor.custom_background = CloudBackground()

        floor.music = None
        floor.sky_texture = BGL.assets.get("KT-forest/texture/starfield1")
        floor.bg_texture = BGL.assets.get("KT-forest/texture/nebula")
        floor.parallax_sky = 0.01
        floor.parallax_bg = 0.04
        floor.fog_level_base = 1.0
        floor.override_base_zoom = 0.2

        floor.uses_vision = True
        return floor

    def build_area_grey_world(self):
        area_raw = BGL.assets.get("KT-forest/textfile/grey_world")
        area_def = get_area_data( area_raw )

        floor = DungeonFloor( 

        bg_texture = BGL.assets.get("KT-forest/texture/grey_world_processed"),
        sky_texture = BGL.assets.get("KT-forest/texture/grey_world_background"),
        parallax_sky = -0.2,
        parallax_bg = 0.04,
        title = "Background Radiation...",
        god_shader = BGL.assets.get("KT-compositor/shader/radiation_god"),
        fog_level_base=0.9, tilescale =2, width = area_def["width"]*2, height = area_def["height"]*2, camera = self.camera, player = self.player, objects = [], area_def = area_def )
        floor.game = self
        return floor


    ###############

    def load_floor( self, key ):

        self.background = Background()
        self.fog = Fog()
        self.area_name = key
        floor = None
        if key == "area_test":
            floor = self.build_area_test()
        if key == "docks":
            floor = self.build_area_docks()
        if key == "tower":
            floor = self.build_area_tower()
        if key == "arena":
            floor = self.build_area_arena()
        if key == "doortest":
            floor = self.build_area_doortest()
        if key == "oort_cloud":
            floor = self.build_area_oort_cloud()
        if key == "ship":
            floor = self.build_area_ship()
        if key == "lacuna_canal":
            floor = self.build_area_lacuna_canal()
        if key == "chase":
            floor = self.build_area_chase()
        if key == "platform":
            floor = self.build_area_platform()
        if key == "kiln":
            floor = self.build_area_kiln()
        if key == "grey_world":
            floor = self.build_area_grey_world()
        if key == "crystals1":
            floor = self.build_area_crystals1()

        if(floor.god_shader):
            Game.god_shader = floor.god_shader

        return floor

    def next_area( self, area_name, target_switch = None, reset = False ):

        self.current_floor_key = area_name
        self.current_floor_target = target_switch
        if area_name == "self":
            area_name = self.area_name
        if (self.area_name is not area_name) or reset:
            #self.tickables.remove( self.floor )
            print("DESTROYING FLOOR")
            self.floor.destroy()
            print("FLOOR IS NONE")
            result = gc.collect()
            print("GC result",result)

            self.floor = self.create_tickable( self.load_floor(area_name) )
            self.player.trigger_title( self.floor.title )
            self.floor.compositor_shader = BGL.assets.get("KT-compositor/shader/compositor")
            self.player.add_dm_message("You teleported")
            
            if "bg_texture" in self.floor.__dict__:
                Background.bg_texture = self.floor.bg_texture
                Background.sky_texture = self.floor.sky_texture
                Background.parallax_sky = self.floor.parallax_sky
                Background.parallax_bg = self.floor.parallax_bg
                if "bg_mode" in self.floor.__dict__:
                    Background.add_blending = True


        #self.player.set_hud_message( "{0} - {1}".format(area_name, target_switch))

        for switch in self.floor.area_switches:
            if switch.switch_name == target_switch:
                self.player.p[0] = switch.p[0]
                self.player.p[1] = switch.p[1]
                switch.trigger_active = False

        self.camera.set_player(self.player)

        self.player.active_terminal = None
        if(self.floor.god_shader):
            Game.god_shader = self.floor.god_shader
        


    def create_player(self):
        return KPlayer( game = self, sight_radius = 90.0, speed = 7.00, controllers = self.controllers, texture = BGL.assets.get("KT-player/texture/player"), size = [ 2.0,2.0] ) 


    def trigger_fade(self, length, color = [ 0.0,0.0,0.0 ]):
        self.max_fade_amt = length
        self.fade_color = color
        self.fade_amt = 0.0

    def initialize(self):
        self.active_cinematic = None
        self.fade_amt = 1.1
        self.max_fade_amt = 1.0
        self.fade_color = [0.0,0.0,0.0]

        self.abilities = Abilities
        self.doing_random_test = False
        self.prebuffer = 0
        self.camera         = self.create_tickable( DungeonCamera( p = [0.0,0.0], zoom = 0.28 ) )
        self.controllers    = self.create_tickable( Controllers() )
        self.player         = self.create_tickable( self.create_player() )

        #areas = generate_qualified_areas()
        #areas = []
        #start_area = filter(lambda x: x.ring==0 and x.depth==0, areas).__next__()
        #start_area.floor = DungeonFloor( width = 90, height = 90, camera = self.camera, player = self.player, objects=[], area=start_area );
        #self.floor          = self.create_tickable( start_area.floor )

        #self.floor = self.create_tickable( Floor() )


        #prime the cache
        ## self.load_floor("area_test")
        ## self.load_floor("tower")
        ## self.load_floor("arena")
        ## self.load_floor("docks")


        ### ENTRY POINT
###########################
        loading_floor = "kiln"
        self.floor = self.create_tickable(self.load_floor(loading_floor))
        self.current_floor_key = loading_floor
        self.current_floor_target = None
        self.player.trigger_title( self.floor.title )
        if "bg_texture" in self.floor.__dict__:
            Background.bg_texture = self.floor.bg_texture
            Background.sky_texture = self.floor.sky_texture
            Background.parallax_sky = self.floor.parallax_sky
            Background.parallax_bg = self.floor.parallax_bg
            if "bg_mode" in self.floor.__dict__:
                Background.add_blending = True

        self.floor.compositor_shader = BGL.assets.get("KT-compositor/shader/compositor")
        self.camera.set_player(self.player)
        self.player_dead_frames = 0

    def render(self):

        if self.active_cinematic:
            self.active_cinematic.render()
        else:
            with BGL.context.render_target( Game.god_buffer):

                BGL.context.clear( 1.0,1.0,1.0,1.0);

                if(self.floor.custom_background):
                    self.floor.custom_background.camera = self.camera
                    self.floor.custom_background.render(self.floor)
                else:
                    self.background.camera = self.camera
                    self.background.render( self.floor.vision_lightmap.get_lightmap_texture()) 
                self.floor.render()
                self.fog.camera = self.camera
                self.fog.render(self.floor, self.floor.vision_lightmap.get_lightmap_texture(),self.floor.fog_level_real+self.floor.fog_level_base) 

            Game.god_buffer.render_processed( Game.god_shader )
            self.player.render_hud()
        if(self.fade_amt< self.max_fade_amt):
            fade_perc = self.fade_amt / self.max_fade_amt

            with BGL.blendmode.alpha_over:
                uniform_fade.apply_fadeout( fade_perc, self.fade_color )

    def tick(self):

        if(self.prebuffer < 30):
            self.prebuffer += 1
            return

        if(self.fade_amt< self.max_fade_amt):
            self.fade_amt += 1.0

        if(self.active_cinematic):
            cinematic_running = self.active_cinematic.tick()
            if not cinematic_running:
                self.active_cinematic = None
            if self.active_cinematic:
                return

        ### 
        ### can uncomment this to test rapid area switching
        ###

        else:
            if self.doing_random_test:
                if(uniform(0.0,1.0)<0.003):
                    area = choice ( [ "ship","grey_world","doortest"] )
                    self.next_area( area, None )
                if(uniform(0.0,1.0)<0.01):
                    self.player.p[0] = uniform( -1*self.floor.width, self.floor.width)
                    self.player.p[1] = uniform( -1*self.floor.height, self.floor.height)

        if(self.floor.freeze_delay < 0):
            if(self.floor.freeze_frames > 0):
                self.floor.freeze_frames = self.floor.freeze_frames - 1
                return
        else:
            self.floor.freeze_delay = self.floor.freeze_delay - 1

        KTState.pad = self.player.get_pad()
        KTState.start_pressed[1] = KTState.start_pressed[0]
        KTState.start_pressed[0] = KTState.pad.button_down(BGL.gamepads.buttons.START)
        
        if(KTState.start_pressed[0]==False) and (KTState.start_pressed[1]==True):
            KTState.paused = not KTState.paused
                
        BaseGame.tick(self)

        if(self.floor.custom_background):
            self.floor.custom_background.tick()

        if self.player.hp <= 0:
            self.player_dead_frames += 1
            if self.player_dead_frames > 220:
                self.player.hp = 100
                self.next_area( self.current_floor_key, self.current_floor_target, True )
                self.player_dead_frames = 0
