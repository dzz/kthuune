from Newfoundland.Camera import Camera
from math import cos,sin
from .KTState import KTState

class DungeonCamera (Camera):

    rate = 0.035

    def __init__(self, **kwargs):
        Camera.__init__(self,**kwargs)
        self.base_zoom = self.zoom
        self.filtered_zoom = self.zoom

    def set_player(self, player):
        self.player = player

    def tick(self):
        if not KTState.paused:
            aim_offset_x = 0.0
            aim_offset_y = 0.0
            isAiming = 0.0
            if(self.player.aiming_beam.aiming):
                isAiming = 1.0

                aim_offset_x = cos( self.player.rad ) * 10
                aim_offset_y = sin( self.player.rad ) * 10

            calc_zoom = self.base_zoom + (self.zoom*(-0.33)*isAiming)
            self.zoom = (self.zoom*0.99) + (calc_zoom*0.01)
            rate = DungeonCamera.rate


            self.p[0] = (self.player.p[0]+aim_offset_x)* rate + ((1.0-rate)*self.p[0])
            self.p[1] = (self.player.p[1]+aim_offset_y)* rate + ((1.0-rate)*self.p[1])
        else:
            self.p[0] = self.p[0] + KTState.pad.leftStick[0]
            self.p[1] = self.p[1] + KTState.pad.leftStick[1]
        
            if(KTState.pad.rightStick[1]<0.1):
                self.zoom = self.zoom * 1.01
            if(KTState.pad.rightStick[1]>-0.1):
                self.zoom = self.zoom * 0.99
