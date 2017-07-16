from Beagle import API as BGL
from Newfoundland.Camera import Camera
from Newfoundland.Controllers import Controllers
from Newfoundland.Player import Player
from Newfoundland.BaseGame import BaseGame

from .DungeonFloor import DungeonFloor
from .DungeonCamera import DungeonCamera
from .KPlayer import KPlayer

from .superstructure import generate_qualified_areas

class Game( BaseGame ):

    def initialize(self):


        self.camera         = self.create_tickable( DungeonCamera( p = [0.0,0.0], zoom = 0.23 ) )
        self.controllers    = self.create_tickable( Controllers() )
        self.player         = self.create_tickable( KPlayer( sight_radius = 40.0, speed = 3.80, controllers = self.controllers, texture = BGL.assets.get("KT-player/texture/player"), size = [ 2.0,2.0] ) )

        areas = generate_qualified_areas()
        start_area = filter(lambda x: x.ring==0 and x.depth==0, areas).__next__()
        start_area.floor = DungeonFloor( width = 300, height = 300, camera = self.camera, player = self.player, objects=[], area=start_area );
        self.floor          = self.create_tickable( start_area.floor )

        #self.floor = self.create_tickable( Floor() )

        self.floor.compositor_shader = BGL.assets.get("KT-compositor/shader/compositor")


        self.camera.set_player(self.player)

    def render(self):
        self.floor.render()

    def tick(self):
        BaseGame.tick(self)
