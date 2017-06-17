from Newfoundland.Camera import Camera

class DungeonCamera (Camera):

    rate = 0.1

    def __init__(self, **kwargs):
        Camera.__init__(self,**kwargs)

    def set_player(self, player):
        self.player = player

    def tick(self):

        rate = DungeonCamera.rate

        self.p[0] = self.player.p[0]* rate + ((1.0-rate)*self.p[0])
        self.p[1] = self.player.p[1]* rate + ((1.0-rate)*self.p[1])
        
