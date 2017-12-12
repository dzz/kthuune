from Newfoundland.Object import Object

class AreaSwitch(Object):
    def customize(self):
        self.visible = False
        self.tick_type = Object.TickTypes.TICK_FOREVER
        self.trigger_active = True
        self.rad2 = 15
        self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
        self.light_color =  [ 2.8,2.7,2.0,1.0]
        self.light_radius = 5.0

    def tick(self):
        dx = self.floor.player.p[0] - self.p[0]
        dy = self.floor.player.p[1] - self.p[1]
        d2 = (dx*dx)+(dy*dy)

        if not self.trigger_active:
            self.light_radius = 0.1
        else:
            if self.light_radius < 5.0:
                self.light_radius = self.light_radius*1.2
        if d2 > (self.rad2*5):

            self.trigger_active = True
        if self.trigger_active:
            if d2 < (self.rad2*10):
                self.floor.player.set_hud_message("go to {0} - {1}".format(self.target_area, self.target_switch))
            if d2 < self.rad2:
                self.trigger()

    def trigger(self):
        self.floor.game.next_area( self.target_area, self.target_switch )
