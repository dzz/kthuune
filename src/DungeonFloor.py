from Beagle import API as BGL
from Newfoundland import Floor, Tilemap
from random import choice
from .Generators.ForestGraveyard import ForestGraveyard

class DungeonFloor( Floor, BGL.auto_configurable):
    def __init__(self,**kwargs):
        BGL.auto_configurable.__init__(self, { "width" : 32, "height" : 32, "generator" : ForestGraveyard()  }, **kwargs )
        beagle_tileset = BGL.tileset(
            texture = BGL.assets.get("KT-tiles/texture/plain_tiles"),
            configuration = {
                "firstgid" : 1,
                "margin" : 0,
                "name" : None,
                "spacing" : 0,
                "tilecount" : 20,
                "tileheight" : 32,
                "tilewidth" : 32
            },
        )


        self.generator.compile( self )

        beagle_tilemap = BGL.tilemap(
            tileset = beagle_tileset,
            configuration = {
                "layers" : [
                    { 
                        "data" : list(map( lambda x: choice(range(1,20)), range(0, self.width*self.height))),
                        "width": self.width,
                        "height": self.height,
                        "name": "floor"
                    }
                ]
            }
        )

        floor_configuration = kwargs
        floor_configuration.update({
            "tilemap" : Tilemap( beagle_tilemap = beagle_tilemap )
        })
        
        Floor.__init__(self,**floor_configuration)
