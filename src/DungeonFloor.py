from Beagle import API as BGL
from Newfoundland.Floor import Floor
from Newfoundland.Tilemap import Tilemap
from Newfoundland.Object import Object
from random import choice
from .Generators.ForestGraveyard import ForestGraveyard, TreeRoots,Fire
from .Generators.BasicGenerator import BasicGenerator
from random import uniform

class Portal(Object):
    def __init__(self,**kwargs):
        overrides = {
                        'light_radius' : 25.0,
                        'light_color' : [ 0.7,1.0,1.0,1.0],
                        'light_type' : Object.LightTypes.DYNAMIC_SHADOWCASTER
                    }
        overrides.update(kwargs)
        Object.__init__(self,**overrides)

class DungeonFloor( Floor, BGL.auto_configurable):
    def __init__(self,**kwargs):
        BGL.auto_configurable.__init__(self,
        {
            "width" : 32,
            "height" : 32,
            #"generator" : ForestGraveyard(),
            "generator" : BasicGenerator(),
            "area" : None,
            "renderer_config" : {
                "vision_lightmap_width" : 256,
                "vision_lightmap_height" : 256,
                "photon_map_width" : 64,
                "photon_map_height" : 64,
                "static_lightmap_width" : 256,
                "static_lightmap_height" : 256,
                "photon_mapper_config" : {
                    'stream' : False,
                    'photon_radius' : 80.0,
                    'photon_emitter_power' : 0.010,
                    'photon_decay' : 0.9,
                    'photon_decay_jitter' : 0.2,
                    'photon_max_bounces' : 5,
                    'num_photons' : 5,
                    'photon_observe_chance' : 0.8
                },
                "compositor_config" : {
                    "photon_buffer_size" : "screen*0.25",
                    "floor_buffer_size" : "screen*2",
                    "light_buffer_size" : "screen*0.5",
                    "object_buffer_size" : "screen",
                    "height_buffer_size" : "screen*0.25",
                    "reflect_buffer_size" : "screen*0.1",
                    "vision_buffer_size" : [256,256]
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

        if(self.area):
            floor_configuration["objects"].extend(self.generate_portal_objects())

        self.light_occluders = self.generator.get_light_occluders()
        self.photon_emitters = self.generator.get_photon_emitters()

        #self.light_occluders = []#self.generator.get_light_occluders()
        #self.photon_emitters = []#self.generator.get_photon_emitters()

        Floor.__init__(self,**floor_configuration)


    def generate_portal_objects(self):
        objs = []
        for portal in self.area.portals:

            if portal.left_area is self.area:
                #portal_p = portal.left_p
                portal_target = portal.right_area
            elif portal.right_area is self.area:
                #portal_p = portal.right_p
                portal_target = portal.left_area

            x = uniform(0.0,self.width/2) -(self.width/4)
            y = uniform(0.0,self.height/2) - (self.height/4)

            portal_object = Portal( p = [x,y], size = [3.0,3.0], portal_target = portal_target )

            print("MADE: ",portal_object, "AT :", portal_object.p)
            objs.append(portal_object)
        return objs

    def get_occluders(self):
        return self.light_occluders

    def get_photon_emitters(self):
        return self.photon_emitters
