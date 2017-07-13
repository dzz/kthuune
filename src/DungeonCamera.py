from Newfoundland.Camera import Camera

class DungeonCamera (Camera):

    rate = 0.1

    def __init__(self, **kwargs):
        Camera.__init__(self,**kwargs)
        self.base_zoom = self.zoom
        self.filtered_zoom = self.zoom

    def set_player(self, player):
        self.player = player

    def tick(self):

        isAiming = 0.0
        if(self.player.aiming_beam.aiming):
            isAiming = 1.0

        calc_zoom = self.base_zoom + (self.zoom*(-0.33)*isAiming)
        self.zoom = (self.zoom*0.99) + (calc_zoom*0.01)
        rate = DungeonCamera.rate

        self.p[0] = self.player.p[0]* rate + ((1.0-rate)*self.p[0])
        self.p[1] = self.player.p[1]* rate + ((1.0-rate)*self.p[1])
        
