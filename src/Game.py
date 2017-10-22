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
from .Fog import Fog

class Game( BaseGame ):

    god_buffer = BGL.framebuffer.from_screen()
    god_shader = BGL.assets.get("KT-compositor/shader/god")

    paused = False
    floor_cache = {}
    area_name = None
    ###############
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

        floor = DungeonFloor( tilescale =2, width = area_def["width"]*2, height = area_def["height"]*2, camera = self.camera, player = self.player, objects = [], area_def = area_def )
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

        floor = DungeonFloor( tilescale =2, width = area_def["width"]*2, height = area_def["height"]*2, camera = self.camera, player = self.player, objects = [], area_def = area_def )
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

    def build_area_ship(self):
        GeneratorOptions.TreeTopTextures = [
            BGL.assets.get("KT-forest/texture/crystal_1"),
            BGL.assets.get("KT-forest/texture/crystal_2"),
            BGL.assets.get("KT-forest/texture/crystal_3"),
            BGL.assets.get("KT-forest/texture/crystal_4")
        ]

        GeneratorOptions.TreeShadowTextures = GeneratorOptions.TreeTopTextures

        area_raw = BGL.assets.get("KT-forest/textfile/ship")
        area_def = get_area_data( area_raw )

        floor = DungeonFloor( 
        title = "The Hunting Pilgrim",
        god_shader = BGL.assets.get("KT-compositor/shader/ship_god"),
        fog_level_base=0.5, tilescale =2, width = area_def["width"]*2, height = area_def["height"]*2, camera = self.camera, player = self.player, objects = [], area_def = area_def )
        floor.game = self
        return floor

    def build_area_grey_world(self):
        area_raw = BGL.assets.get("KT-forest/textfile/grey_world")
        area_def = get_area_data( area_raw )

        floor = DungeonFloor( 

        bg_texture = BGL.assets.get("KT-forest/texture/grey_world_processed"),
        sky_texture = BGL.assets.get("KT-forest/texture/grey_world_background"),
        parallax_sky = -0.2,
        parallax_bg = 0.005,
        title = "Background Radiation...",
        god_shader = BGL.assets.get("KT-compositor/shader/radiation_god"),
        fog_level_base=0.9, tilescale =2, width = area_def["width"]*2, height = area_def["height"]*2, camera = self.camera, player = self.player, objects = [], area_def = area_def )
        floor.game = self
        return floor


    ###############

    def load_floor( self, key ):

        self.background = Background()
        self.fog = Fog()
        Game.floor_cache = {}
        cache_hit = False
        self.area_name = key
        if not key in Game.floor_cache:
            if key == "area_test":
                Game.floor_cache[key] = self.build_area_test()
            if key == "docks":
                Game.floor_cache[key] = self.build_area_docks()
            if key == "tower":
                Game.floor_cache[key] = self.build_area_tower()
            if key == "arena":
                Game.floor_cache[key] = self.build_area_arena()
            if key == "doortest":
                Game.floor_cache[key] = self.build_area_doortest()
            if key == "oort_cloud":
                Game.floor_cache[key] = self.build_area_oort_cloud()
            if key == "ship":
                Game.floor_cache[key] = self.build_area_ship()
            if key == "grey_world":
                Game.floor_cache[key] = self.build_area_grey_world()
        else:
            cache_hit = True

        Game.floor_cache[key].reattach_player()

        if cache_hit:
            Game.floor_cache[key].reinitialize_physics()

        if(Game.floor_cache[key].god_shader):
            Game.god_shader = Game.floor_cache[key].god_shader

        return Game.floor_cache[key]            

    def next_area( self, area_name, target_switch ):
        if area_name == "self":
            area_name = self.area_name
        if self.area_name is not area_name:
            self.tickables.remove( self.floor )
            self.floor = self.create_tickable( self.load_floor(area_name) )
            self.player.trigger_title( self.floor.title )
            self.floor.compositor_shader = BGL.assets.get("KT-compositor/shader/compositor")
            
            if "bg_texture" in self.floor.__dict__:
                Background.bg_texture = self.floor.bg_texture
                Background.sky_texture = self.floor.sky_texture
                Background.parallax_sky = self.floor.parallax_sky
                Background.parallax_bg = self.floor.parallax_bg


        self.player.set_hud_message( "{0} - {1}".format(area_name, target_switch))

        for switch in self.floor.area_switches:
            if switch.switch_name == target_switch:
                self.player.p[0] = switch.p[0]
                self.player.p[1] = switch.p[1]
                switch.trigger_active = False

        self.camera.set_player(self.player)
        Game.god_shader = self.floor.god_shader
        


    def create_player(self):
        return KPlayer( sight_radius = 90.0, speed = 7.00, controllers = self.controllers, texture = BGL.assets.get("KT-player/texture/player"), size = [ 2.0,2.0] ) 

    def initialize(self):

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

        self.floor = self.create_tickable(self.load_floor("doortest"))
        self.player.trigger_title( self.floor.title )
        if "bg_texture" in self.floor.__dict__:
            Background.bg_texture = self.floor.bg_texture
            Background.sky_texture = self.floor.sky_texture
            Background.parallax_sky = self.floor.parallax_sky
            Background.parallax_bg = self.floor.parallax_bg

        self.floor.compositor_shader = BGL.assets.get("KT-compositor/shader/compositor")
        self.camera.set_player(self.player)

    def render(self):
        with BGL.context.render_target( Game.god_buffer):

            BGL.context.clear( 1.0,1.0,1.0,1.0);
            self.background.camera = self.camera
            self.background.render( self.floor.vision_lightmap.get_lightmap_texture()) 
            #with BGL.blendmode.alpha_over:
            self.floor.render()
            self.fog.camera = self.camera
            self.fog.render(self.floor, self.floor.vision_lightmap.get_lightmap_texture(),self.floor.fog_level_real+self.floor.fog_level_base) 

        Game.god_buffer.render_processed( Game.god_shader )
        self.player.render_hud()

    def tick(self):

        if(self.prebuffer < 30):
            self.prebuffer += 1
            return

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
