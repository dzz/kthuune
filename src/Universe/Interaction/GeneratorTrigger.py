from Newfoundland.Object import Object

class GeneratorTrigger(Object):
    def parse(od,df):
        gen_mode = od["key"]
        x1 = od["x"]
        x2 = od["x"] + od["w"]
        y1 = od["y"]
        y2 = od["y"] + od["h"]
        return GeneratorTrigger( x1 = x1, y1 = y1, x2 = x2, y2 = y2, gen_mode = gen_mode )        

    def customize(self):
        self.visible = False
        self.tick_type = Object.TickTypes.TICK_FOREVER
        self.last_pp = None

    def snapshot_player(self):
        self.last_pp = [ self.floor.player.p[0], self.floor.player.p[1] ]

    def tick(self):

        if self.last_pp is None:
            self.snapshot_player()
        else:
            if self.gen_mode == "generator_above":
                if (self.last_pp[0] > self.x1) and (self.last_pp[0]< self.x2):
                    if(self.last_pp[1] > self.y1) and (self.floor.player.p[1] < self.y1):
                        self.floor.new_area_up(self)
            elif self.gen_mode == "generator_below":
                if (self.last_pp[0] > self.x1) and (self.last_pp[0]< self.x2):
                    if(self.last_pp[1] < self.y1) and (self.floor.player.p[1] > self.y1):
                        self.floor.new_area_down(self)
            elif self.gen_mode == "generator_left":
                if (self.last_pp[1] > self.y1) and (self.last_pp[1] < self.y2):
                    if(self.last_pp[0] > self.x1) and (self.floor.player.p[0] < self.x1):
                        self.floor.new_area_left(self)
            elif self.gen_mode == "generator_right":
                if (self.last_pp[1] > self.y1) and (self.last_pp[1] < self.y2):
                    if(self.last_pp[0] < self.x1) and (self.floor.player.p[0] > self.x1):
                        self.floor.new_area_right(self)

            self.snapshot_player()
            

