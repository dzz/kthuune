from Newfoundland.Camera import Camera
from math import cos,sin
from .KTState import KTState

class DungeonCamera (Camera):

    LOCK_AXIS_X = 0
    LOCK_AXIS_Y = 1
    LOCK_AXIS_BOTH = 2
    ZOOM_NONE = -1
 
    rate = 0.2

    def __init__(self, **kwargs):
        Camera.__init__(self,**kwargs)
        self.base_zoom = self.zoom
        self.filtered_zoom = self.zoom

    def set_player(self, player):
        self.player = player
        self.p[0] = self.player.p[0]
        self.p[1] = self.player.p[1]

    def tick(self):
        if not KTState.paused:
            aim_offset_x = 0.0
            aim_offset_y = 0.0
            isAiming = 0.0
            if(self.player.aiming_beam.aiming):
                isAiming = 1.0

                aim_offset_x = cos( self.player.rad ) * 10
                aim_offset_y = sin( self.player.rad ) * 10


            sx = self.player.v[0]
            sy = self.player.v[1]
            sc = 0.4 / (1.0 + ((sx*sx)+(sy*sy)))

            if self.player.link_count == 0:
                rate = DungeonCamera.rate
            else:
                rate = 0.1


            pad = self.player.controllers.get_virtualized_pad( self.player.num )

            aim_offset_x = (pad.right_stick[0]*12) + (self.player.v[0]*0.5)
            aim_offset_y = (pad.right_stick[1]*12) + (self.player.v[1]*0.5)


            pX = self.player.p[0]
            pY = self.player.p[1]

            activeRegion = None
            for region in self.player.floor.camera_lock_regions:
                if pX > region[0] and pX < region[2] and pY > region[1] and pY < region[3]:
                    activeRegion = region
                    break
                    
            if activeRegion:
                rate *= 0.3
                if activeRegion[4] == DungeonCamera.LOCK_AXIS_X:
                    pY = (region[1]+region[3])/2
                if activeRegion[4] == DungeonCamera.LOCK_AXIS_Y:
                    pX = (region[0]+region[2])/2
                if activeRegion[4] == DungeonCamera.LOCK_AXIS_BOTH:
                    pX = (region[0]+region[2])/2
                    pY = (region[1]+region[3])/2

            self.p[0] = (pX+aim_offset_x)* rate + ((1.0-rate)*self.p[0])
            self.p[1] = (pY+aim_offset_y)* rate + ((1.0-rate)*self.p[1])

            calc_zoom = (self.base_zoom + (self.zoom*(-0.33)*isAiming) + sc)*0.6

            if(self.player.snap_animation_buffer>0):
                calc_zoom *= 2.7

            if activeRegion:
                calc_zoom *= 0.8

            if(self.zoom < calc_zoom):
                self.zoom = (self.zoom*0.999) + (calc_zoom*0.001)
            else:
                self.zoom = (self.zoom*0.99) + (calc_zoom*0.01)


        else:
            self.p[0] = self.p[0] + KTState.pad.leftStick[0]
            self.p[1] = self.p[1] + KTState.pad.leftStick[1]
        
            if(KTState.pad.rightStick[1]<0.1):
                self.zoom = self.zoom * 1.01
            if(KTState.pad.rightStick[1]>-0.1):
                self.zoom = self.zoom * 0.99
