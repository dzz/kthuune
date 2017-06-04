from Newfoundland import Camera, Controllers, Player, BaseGame, Floor
from Beagle import API as BGL

from .DungeonFloor import DungeonFloor

class Game( BaseGame ):

    def initialize(self):
        self.camera         = self.create_tickable( Camera( p = [0.0,0.0], zoom = 0.25 ) )
        self.controllers    = self.create_tickable( Controllers() )
        self.player         = self.create_tickable( Player( controllers = self.controllers, texture = BGL.assets.get("KT-player/texture/player"), size = [ 1.0,1.0] ) )
        self.floor          = self.create_tickable( DungeonFloor( width = 128, height = 128, camera = self.camera, player = self.player, objects=[] ) )

        self.floor.compositor_shader = BGL.assets.get("KT-compositor/shader/compositor")


        self.player.p = [ 0, 0 ]
        self.camera.p = self.player.p

    def render(self):
        self.floor.render()

    def tick(self):
        BaseGame.tick(self)

