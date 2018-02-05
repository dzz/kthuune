from Newfoundland.Object import Object

class TotemContainer(Object):
    def parse(od,df):
        region = ( od["x"], od["y"], od["x"]+od["w"], od["y"]+od["h"], axes, zoom )
        return TotemContainer( p = [ od["x"],od["y"], region = region )

    def customize(self):
        self.visible = False
        self.tick_type = Object.TickTypes.PURGING
        self.charged = False

    def tick(self):
        charged = True
        for totem in self.floor.totems:
            if totem.p[0] > self.region[0] and totem.p[0] < self.region[2] and totem.p[1] > self.region[1] and totem.p[1] < self.region[3]:
                if totem.reset_timer < 0:
                    charged = False
                    break
        if charged:
            self.charged = True
            return False
        return True

