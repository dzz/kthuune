from Beagle import API as BGL
from Newfoundland.Controllers import Controllers
from Newfoundland.Camera import Camera

from ..Universe.AreaLoader import get_area_data
from ..DungeonFloor import DungeonFloor
from ..KPlayer import KPlayer
from .Grid import Grid

class PreviewCamera(Camera):
    def __init__(self, **kwargs):
        Camera.__init__(self,**kwargs)
        self.cinema_target = None
        self.cinema_timeout = 0
        self.cinema_callback = None

    def grab_cinematic(self, obj, timeout, callback = None ):
        pass
        #self.cinema_target = obj
        #self.cinema_timeout = timeout
        #self.cinema_callback = callback
    

class LevelPreview:

    tpx = None
    playercam = False
    camera = PreviewCamera()
    controllers = Controllers()
    player = None
    floor = None

    def create_player():
        return KPlayer( game = LevelPreview, sight_radius = 90.0, speed = 7.00, controllers = LevelPreview.controllers, texture = BGL.assets.get("KT-player/texture/player"), size = [ 2.0,2.0] ) 

    def reset(area_raw):
        LevelPreview.player = LevelPreview.create_player()
        area_def = get_area_data(area_raw)
        LevelPreview.floor = DungeonFloor( game = LevelPreview, tilescale =2, width = area_def["width"]*2, height = area_def["height"]*2, camera = LevelPreview.camera, player = LevelPreview.player, objects = [], area_def = area_def )



    def tick(app):
        if LevelPreview.floor:
            LevelPreview.player.tick()
            LevelPreview.controllers.tick()
            if(LevelPreview.floor.freeze_delay < 0):
                if(LevelPreview.floor.freeze_frames > 0):
                    LevelPreview.floor.freeze_frames = LevelPreview.floor.freeze_frames - 1
            else:
                LevelPreview.floor.freeze_delay = LevelPreview.floor.freeze_delay - 1

            LevelPreview.floor.tick()

            if LevelPreview.tpx is not None:
                LevelPreview.player.p[0] = LevelPreview.tpx
                LevelPreview.player.p[1] = LevelPreview.tpy
                LevelPreview.tpx = None


    def toggle_camlock():
        LevelPreview.playercam = not LevelPreview.playercam


    def orient_player():
        if LevelPreview.floor is not None:
            LevelPreview.player.p[0] = Grid.cx*2
            LevelPreview.player.p[1] = Grid.cx*2

    def synch_cams(app):
        yoffs = -940
        if LevelPreview.floor is not None:
            if(LevelPreview.playercam):
                LevelPreview.camera.p[0] = LevelPreview.player.p[0]
                LevelPreview.camera.p[1] = LevelPreview.player.p[1] + yoffs
                Grid.cx = LevelPreview.player.p[0]*0.5
                Grid.cy = (LevelPreview.player.p[1]*0.5) + yoffs

    def stash_player():
        if(LevelPreview.floor is not None):
            LevelPreview.tpx = LevelPreview.player.p[0]
            LevelPreview.tpy = LevelPreview.player.p[1]

    def render(app):
        LevelPreview.camera.p[0] = Grid.cx*2
        LevelPreview.camera.p[1] = Grid.cy*2
        LevelPreview.camera.zoom = Grid.zoom*0.5
        if LevelPreview.floor is not None:
            if(LevelPreview.playercam):
                LevelPreview.camera.p[0] = LevelPreview.player.p[0]
                LevelPreview.camera.p[1] = LevelPreview.player.p[1]
                Grid.cx = LevelPreview.player.p[0]*0.5
                Grid.cy = LevelPreview.player.p[1]*0.5
                app.camera_x = Grid.cx
                app.camera_y = Grid.cy

            LevelPreview.floor.guppyRenderer.gup_count = 0
            LevelPreview.floor.precompute_frame()
            LevelPreview.floor.render_preview()
            LevelPreview.player.render_hud(False)
            LevelPreview.floor.gup_count = LevelPreview.floor.guppyRenderer.gup_count


