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
        self.base_zoom*=1.1
        self.filtered_zoom = self.zoom
        self.cinema_target = None
        self.cinema_timeout = 0
        self.cinema_callback = None
        

    def grab_cinematic(self, obj, timeout, callback = None ):
        self.cinema_target = obj
        self.cinema_timeout = timeout
        self.cinema_callback = callback

    def set_player(self, player):
        self.player = player
        self.p[0] = self.player.p[0]
        self.p[1] = self.player.p[1]

    def get_forced_offset(self):
        return self.player.floor.get_forced_offset()

    def tick(self):

        if self.cinema_target:
            if "message" in self.cinema_target.__dict__:
                print(self.cinema_target.message)
                print(self.cinema_target.p)
        if not KTState.paused:
            aim_offset_x = 0.0
            aim_offset_y = 0.0
            isAiming = 0.0
            #if(self.player.aiming_beam.aiming):
            #    isAiming = 1.0
            #   aim_offset_x = cos( self.player.rad ) * 10
            #   aim_offset_y = sin( self.player.rad ) * 10


            sx = self.player.v[0]
            sy = self.player.v[1]
            sc = 0.4 / (1.0 + ((sx*sx)+(sy*sy)))

            if self.player.link_count == 0:
                rate = DungeonCamera.rate
            else:
                rate = 0.1


            pad = self.player.controllers.get_virtualized_pad( self.player.num )

            if(abs(pad.right_stick[0]) < 0.1): pad.right_stick[0] = 0.0
            if(abs(pad.right_stick[1]) < 0.1): pad.right_stick[1] = 0.0

            aim_offset_x = (pad.right_stick[0]*5) + (self.player.v[0]*0.2)
            aim_offset_y = (pad.right_stick[1]*5) + (self.player.v[1]*0.2)

            if not self.cinema_target:
                fo = self.get_forced_offset()
                if not fo:
                    pX = self.player.p[0] + (self.player.v[0]*0.15)
                    pY = self.player.p[1] + (self.player.v[1]*0.15)
                else:
                    pX = fo[0]
                    pY = fo[1]
            else:
                pX = self.cinema_target.p[0]
                pY = self.cinema_target.p[1]
                self.cinema_timeout -= 1
                if self.cinema_timeout == 0:
                    self.cinema_target = None
                    if(self.cinema_callback):
                        self.cinema_callback()

            if not self.cinema_target:
                if(self.player.active_terminal):
                    pX += 15

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


            #if not self.player.floor.blurring:
            if True:
                self.p[0] = (pX+aim_offset_x)* rate + ((1.0-rate)*self.p[0])
                self.p[1] = (pY+aim_offset_y)* rate + ((1.0-rate)*self.p[1])


            if ( self.player.floor.override_base_zoom):
                bz = self.player.floor.override_base_zoom
            else:
                bz = self.base_zoom

            calc_zoom = (bz + (self.zoom*(-0.33)*isAiming) + sc)*0.8

            if(self.player.snap_animation_buffer>0):
                calc_zoom *= 2.7

            if activeRegion:
                calc_zoom *= 0.8

            if not self.cinema_target:
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
