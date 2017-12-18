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

class LevelPreview:

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

    def render(app):
        LevelPreview.camera.p[0] = Grid.cx*2
        LevelPreview.camera.p[1] = Grid.cy*2
        LevelPreview.camera.zoom = Grid.zoom*0.5
        if LevelPreview.floor is not None:
            LevelPreview.floor.precompute_frame()
            LevelPreview.floor.render_preview()


