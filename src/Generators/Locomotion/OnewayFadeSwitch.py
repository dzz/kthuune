from Newfoundland.Object import Object

class OnewayFadeSwitch(Object):
    def parse(od, df):
        if "radius" in od["meta"]:
            radius = float(od["meta"]["radius"])
        else:
            radius = 5
            
        return OnewayFadeSwitch(trigger_radius=radius, p=[od["x"],od["y"]], target_area = od["meta"]["target"])

    def customize(self):
        self.visible = False
        self.tick_type = Object.TickTypes.PURGING
        self.fade_time = 60
        self.triggered = False

    def tick(self):
        if self.mdist( self.floor.player )< self.trigger_radius:
            self.triggered = True
            def next_callback():
                self.floor.game.next_area( self.target_area, None )
            self.floor.camera.grab_cinematic( self, self.fade_time, next_callback )
            self.floor.game.trigger_fade( self.fade_time )
            return False
        return True
