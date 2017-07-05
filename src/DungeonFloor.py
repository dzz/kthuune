from Beagle import API as BGL
from Newfoundland.Floor import Floor
from Newfoundland.Tilemap import Tilemap
from Newfoundland.Object import Object
from random import choice
from .Generators.ForestGraveyard import ForestGraveyard, TreeRoots,Fire
from .Generators.BasicGenerator import BasicGenerator
from random import uniform
from math import sin,cos,hypot


class Portal(Object):
    def __init__(self,**kwargs):
        overrides = {
                        "texture" : BGL.assets.get('KT-forest/texture/portal'),
                        'light_radius' : 25.0,
                        'size': [ 13.0, 13.0] ,
                        'light_color' : [ 0.7,1.0,1.0,1.0],
                        'rad' : uniform(-3.14,3.14),
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
            "generator" : ForestGraveyard(),
            #"generator" : BasicGenerator(),
            "area" : None,
            "renderer_config" : {
                "vision_lightmap_width" : 512,
                "vision_lightmap_height" : 512,
                "photon_map_width" : 256,
                "photon_map_height" : 256,
                "static_lightmap_width" : 512,
                "static_lightmap_height" : 512,
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
                    "photon_buffer_size" : "screen",
                    "floor_buffer_size" : "screen",
                    "light_buffer_size" : "screen",
                    "object_buffer_size" : "screen",
                    "height_buffer_size" : "screen",
                    "reflect_buffer_size" : "screen",
                    "vision_buffer_size" : "screen"
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


        if self.area:
            pobjs = self.generate_portal_objects()
            self.generator.compile( self, pobjs  )
        else:
            self.generator.compile( self, []  )

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

        #self.light_occluders = []#self.generator.get_light_occluders()
        #self.photon_emitters = []#self.generator.get_photon_emitters()

        Floor.__init__(self,**floor_configuration)


    def generate_portal_objects(self):
        #objs = []

        #rad = 0.0
        #rad_delt = (3.14*2)/float(len(self.area.portals))
        #min_d = self.width/50.0;
        #max_d = self.width/2.5;

        #for portal in self.area.portals:

        #    if portal.left_area is self.area:
        #        #portal_p = portal.left_p
        #        portal_target = portal.right_area
        #    elif portal.right_area is self.area:
        #        #portal_p = portal.right_p
        #        portal_target = portal.left_area

        #    d = uniform(min_d,max_d)
        #    x = cos(rad)*d;
        #    y = sin(rad)*d;

        #    rad = rad+rad_delt
        #    portal_object = Portal( p = [x,y], portal_target = portal_target )

        #    print("MADE: ",portal_object, "AT :", portal_object.p)
        #    objs.append(portal_object)

        objs = []

        idx = 0
        while len(objs) is not len(self.area.portals):
            min_dist = 25
            portal = self.area.portals[idx]
            if portal.left_area is self.area:
                #portal_p = portal.left_p
                portal_target = portal.right_area
            elif portal.right_area is self.area:
                #portal_p = portal.right_p
                portal_target = portal.left_area


            tx = uniform(-self.width,self.width)*0.5
            ty = uniform(-self.height,self.height)*0.5
           
            for obj in objs:
                if hypot( tx-obj.p[0], ty-obj.p[1])<min_dist: 
                    continue
            portal_object = Portal( p = [tx,ty], portal_target = portal_target )
            objs.append(portal_object)
            idx = idx + 1
 
        return objs

    def get_occluders(self):
        return self.light_occluders

    def get_photon_emitters(self):
        return self.photon_emitters
