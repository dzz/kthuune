from Newfoundland import Camera, Controllers, Player, Floor, BaseGame

class Game( BaseGame ):

    def initialize(self):
        self.camera         = self.create_tickable( Camera( p = [0.0,0.0], zoom = 0.25 ) )
        self.controllers    = self.create_tickable( Controllers() )
        self.player         = self.create_tickable( Player( controllers = self.controllers ) )
        self.floor          = self.create_tickable( Floor( width = 64, height = 64, camera = self.camera, player = self.player ) )

        self.player.p = [ -4,-4 ]
        self.camera.p = self.player.p

    def render(self):
        self.floor.render()

    def tick(self):
        BaseGame.tick(self)

