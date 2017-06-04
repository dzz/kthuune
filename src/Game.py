from Newfoundland import Camera, Controllers, Player, BaseGame, Floor
from Beagle import API as BGL

from .DungeonFloor import DungeonFloor
from .DungeonCamera import DungeonCamera


class Game( BaseGame ):

    def initialize(self):
        self.camera         = self.create_tickable( DungeonCamera( p = [0.0,0.0], zoom = 0.666 ) )
        self.controllers    = self.create_tickable( Controllers() )
        self.player         = self.create_tickable( Player( speed = 0.07, controllers = self.controllers, texture = BGL.assets.get("KT-player/texture/player"), size = [ 1.0,1.0] ) )
        self.floor          = self.create_tickable( DungeonFloor( width = 64, height = 64, camera = self.camera, player = self.player, objects=[] ) )

        self.floor.compositor_shader = BGL.assets.get("KT-compositor/shader/compositor")


        self.camera.set_player(self.player)

    def render(self):
        self.floor.render()

    def tick(self):
        BaseGame.tick(self)

