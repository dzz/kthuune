from Newfoundland.Object import Object

class Breakable(Object):
    def handle_pull(self):
        dx = self.p[0] - self.floor.player.p[0]
        dy = self.p[1] - self.floor.player.p[1]
        self.floor.player.v[0] += dx * 2.2
        self.floor.player.v[1] += dy * 2.2
