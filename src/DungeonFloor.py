from Beagle import API as BGL
from Newfoundland import Floor

class DungeonFloor( Floor, BGL.auto_configurable):
    def __init__(self,**kwargs):
        Floor.__init__(self,**kwargs)
