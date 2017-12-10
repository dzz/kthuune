from Newfoundland.Object import Object
from random import uniform, choice
from ..Enemies.Worm import Worm

class WormField(Object):
    def parse(od,df):
        return WormField( wf_spec = [ od['x'],od['y'],10.0] )

    def customize(self):
        self.tick_type = Object.TickTypes.PURGING
        self.buftarget = "popup"
        self.visible = False

        self.p[0] = self.wf_spec[0]
        self.p[1] = self.wf_spec[1]
        self.wf_radius = self.wf_spec[2]
        self.worms = []

    def tick(self):
        if(len(self.worms)<choice([4,5,6])):
            worm = Worm( p = [self.p[0],self.p[1] ] )
            self.worms.append(worm)
            self.floor.snap_enemies.append(worm)
            self.floor.create_object(worm)
            return True
        return False
