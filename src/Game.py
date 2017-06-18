from Beagle import API as BGL
from Newfoundland.Camera import Camera
from Newfoundland.Controllers import Controllers
from Newfoundland.Player import Player
from Newfoundland.Floor import Floor
from Newfoundland.BaseGame import BaseGame

from .DungeonFloor import DungeonFloor
from .DungeonCamera import DungeonCamera
from .KPlayer import KPlayer


class Game( BaseGame ):

    def initialize(self):
        self.camera         = self.create_tickable( DungeonCamera( p = [0.0,0.0], zoom = 0.3 ) )
        self.controllers    = self.create_tickable( Controllers() )
        self.player         = self.create_tickable( KPlayer( sight_radius = 70.0, speed = 2.00, controllers = self.controllers, texture = BGL.assets.get("KT-player/texture/player"), size = [ 1.0,1.0] ) )
        self.floor          = self.create_tickable( DungeonFloor( width = 512, height = 512, camera = self.camera, player = self.player, objects=[] ) )

        self.floor.compositor_shader = BGL.assets.get("KT-compositor/shader/compositor")


        self.camera.set_player(self.player)

    def render(self):
        self.floor.render()

    def tick(self):
        BaseGame.tick(self)

