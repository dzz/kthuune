from Beagle import API as BGL
from Newfoundland.Floor import Floor
from Newfoundland.Tilemap import Tilemap
from random import choice
from .Generators.ForestGraveyard import ForestGraveyard

class DungeonFloor( Floor, BGL.auto_configurable):
    def __init__(self,**kwargs):
        BGL.auto_configurable.__init__(self, 
        { 
            "width" : 32, 
            "height" : 32, 
            "generator" : ForestGraveyard(),
            "renderer_config" : {
                "vision_lightmap_width" : 64,
                "vision_lightmap_height" : 64,
                "photon_map_width" : 512,
                "photon_map_height" : 512,
                "static_lightmap_width" : 1024,
                "static_lightmap_height" : 1024,
                "photon_mapper_config" : { 
                    'stream' : False,
                    'photon_radius' : 180.0,
                    'photon_emitter_power' : 0.012,
                    'photon_decay' : 0.90,
                    'photon_decay_jitter' : 0.2,
                    'photon_max_bounces' : 8,
                    'num_photons' : 30,
                    'photon_observe_chance' : 0.15
                }
            }
        }, **kwargs )
        beagle_tileset = BGL.tileset(
            texture = BGL.assets.get("KT-tiles/texture/dungeon_tiles"),
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
                        "data" : self.generator.get_tiledata(),
                        "width": self.width,
                        "height": self.height,
                        "name": "floor"
                    }
                ]
            }
        )

        floor_configuration = kwargs
        floor_configuration.update({
            "tilemap" : Tilemap( beagle_tilemap = beagle_tilemap, channel_textures = {
                "height" : BGL.assets.get("KT-tiles/texture/plain_tiles"),
                "reflection" : BGL.assets.get("KT-tiles/texture/plain_tiles")
            } ),
            "objects" : self.generator.get_objects(),
            "renderer_config" : self.renderer_config
        })
        
        self.light_occluders = self.generator.get_light_occluders()
        self.photon_emitters = self.generator.get_photon_emitters()

        Floor.__init__(self,**floor_configuration)

    def get_occluders(self):
        return self.light_occluders
    
    def get_photon_emitters(self):
        return self.photon_emitters
