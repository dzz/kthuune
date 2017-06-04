from Beagle import API as BGL
from Newfoundland import Floor, Tilemap

class DungeonFloor( Floor, BGL.auto_configurable):
    def __init__(self,**kwargs):
        BGL.auto_configurable.__init__(self, { "width" : 32, "height" : 32 }, **kwargs )
        beagle_tileset = BGL.tileset(
            texture = BGL.assets.get("KT-tiles/texture/dungeon_tiles"),
            configuration = {
                "firstgid" : 1,
                "margin" : 0,
                "name" : "dungeon_tiles",
                "spacing" : 0,
                "tilecount" : 20,
                "tileheight" : 16,
                "tilewidth" : 16
            },
        )

        beagle_tilemap = BGL.tilemap(
            tileset = beagle_tileset,
            configuration = {
                "layers" : [
                    { 
                        "data" : [1]*(self.width*self.height),
                        "width": self.width,
                        "height": self.height,
                        "name": "floor",
                        "tileheight" : 32,
                        "tilewidth" : 32
                    }
                ]
            }
        )

        floor_configuration = kwargs
        floor_configuration.update({
            "tilemap" : Tilemap( beagle_tilemap = beagle_tilemap )
        })
        
        Floor.__init__(self,**floor_configuration)
