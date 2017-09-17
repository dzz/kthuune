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

from .Background import Background
from .Fog import Fog

class Game( BaseGame ):

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
        else:
            cache_hit = True

        Game.floor_cache[key].reattach_player()

        if cache_hit:
            Game.floor_cache[key].reinitialize_physics()
        return Game.floor_cache[key]            

    def next_area( self, area_name, target_switch ):
        if area_name == "self":
            area_name = self.area_name
        if self.area_name is not area_name:
            self.tickables.remove( self.floor )
            self.floor = self.create_tickable( self.load_floor(area_name) )
            self.floor.compositor_shader = BGL.assets.get("KT-compositor/shader/compositor")

        self.player.set_hud_message( "{0} - {1}".format(area_name, target_switch))

        for switch in self.floor.area_switches:
            if switch.switch_name == target_switch:
                self.player.p[0] = switch.p[0]
                self.player.p[1] = switch.p[1]
                switch.trigger_active = False

        self.camera.set_player(self.player)
        


    def create_player(self):
        return KPlayer( sight_radius = 40.0, speed = 8.40, controllers = self.controllers, texture = BGL.assets.get("KT-player/texture/player"), size = [ 2.0,2.0] ) 

    def initialize(self):

        self.camera         = self.create_tickable( DungeonCamera( p = [0.0,0.0], zoom = 0.35 ) )
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

        self.floor.compositor_shader = BGL.assets.get("KT-compositor/shader/compositor")
        self.camera.set_player(self.player)

    def render(self):
        self.background.camera = self.camera
        self.background.render() 
        with BGL.blendmode.alpha_over:
            self.floor.render()
        self.fog.camera = self.camera
        self.fog.render(self.floor) 
        self.player.render_hud()

    def tick(self):

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
