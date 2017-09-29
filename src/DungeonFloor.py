from Beagle import API as BGL
from Newfoundland.Floor import createFloorClass
from Newfoundland.Tilemap import Tilemap
from Newfoundland.Object import Object
from random import choice
from .Generators.ForestGraveyard import ForestGraveyard, TreeRoots,Fire
from .Generators.BasicGenerator import BasicGenerator
from .Renderers.DFRenderer import DFRenderer
from random import uniform
from math import sin,cos,hypot
from .AimingBeam import AimingBeam
from .AimingBeam import LazerBeam
from .KTState import KTState
import client.system.keyboard as keyboard


class Portal(Object):
    def __init__(self,**kwargs):
        overrides = {
                        "texture" : BGL.assets.get('KT-forest/texture/portal'),
                        'light_radius' : 65.0,
                        'size': [ 13.0, 13.0] ,
                        'light_color' : [ 0.2,0.4,0.4,0.4],
                        'rad' : uniform(-3.14,3.14),
                        'light_type' : Object.LightTypes.DYNAMIC_SHADOWCASTER,
                        'tick_type' : Object.TickTypes.TICK_FOREVER,
                        "buftarget" : "floor"
                    }
        overrides.update(kwargs)
        Object.__init__(self,**overrides)

    def tick(self):
        self.rad = self.rad + 0.001


Floor = createFloorClass( DFRenderer )
class DungeonFloor( Floor ):
    def __init__(self,**kwargs):
        BGL.auto_configurable.__init__(self,
        {
            "freeze_frames" : 0,
            "freeze_delay" : 0,
            "doors" : [],
            "snap_enemies" : [],
            "using_tilemap" : True,
            "tilescale" : 3,
            "area_def" : None,
            "width" : 32,
            "height" : 32,
            "generator" : ForestGraveyard(),
            #"generator" : BasicGenerator(),
            "area" : None,
            "renderer_config" : {
                "vision_lightmap_width" : 960,
                "vision_lightmap_height" : 540,
                "photon_map_width" : 1024,
                "photon_map_height" : 1024,
                "static_lightmap_width" : 1024,
                "static_lightmap_height" : 1024,
                "dynamic_lightmap_width" : 960,
                "dynamic_lightmap_height" : 540,
                "photon_mapper_config" : {
                    'stream' : True,
                    'photon_radius' :70.0,
                    'photon_emitter_power' : 0.01,
                    'photon_decay' : 0.9,
                    'photon_decay_jitter' : 0.4,
                    'photon_max_bounces' : 9,
                    'num_photons' : 8,
                    'photon_observe_chance' : 0.8
                },
                "physics" : {
                    "timestep_divisions" : 2.0,
                    "solver_iterations" : 2.0,
                    "wall_friction" : 0.2
                }
            }
        }, **kwargs )
        beagle_tileset = BGL.tileset(
            texture = BGL.assets.get("KT-tiles/texture/floor_tiles"),
            configuration = {
                "firstgid" : 1,
                "margin" : 0,
                "name" : None,
                "spacing" : 0,
                "tilecount" : 70,
                "tileheight" : 32,
                "tilewidth" : 32
            },
        )


        #self.tilescale = 3
        self.tilemap_width = int(self.width/self.tilescale)
        self.tilemap_height = int(self.height/self.tilescale)

        self.reflection_map = BGL.assets.get("KT-forest/texture/lightmap")
        if self.area:
            #pobjs = self.generate_portal_objects()
            pobjs = []
            self.generator.compile( self, pobjs  )
        else:
            self.generator.compile( self, []  )

        beagle_tilemap = BGL.tilemap(
            tileset = beagle_tileset,
            configuration = {
                "layers" : [
                    {
                        "data" : self.generator.get_tiledata(),
                        "width": self.tilemap_width,
                        "height": self.tilemap_height,
                        "name": "floor"
                    }
                ]
            }
        )

        floor_configuration = kwargs
        floor_configuration.update({
            "tilemap" : Tilemap( tilescale = self.tilescale, beagle_tilemap = beagle_tilemap, channel_textures = {
                "height" : BGL.assets.get("KT-tiles/texture/plain_tiles"),
                "reflection" : BGL.assets.get("KT-tiles/texture/plain_tiles")
            } ),
            "objects" : self.generator.get_objects(),
            "renderer_config" : self.renderer_config,
            "light_occluders" : self.generator.get_light_occluders(),
            "physics_occluders" : self.generator.get_physics_occluders(),
            "photon_emitters" :  self.generator.get_photon_emitters()
        })

       
        self.player.aiming_beam = AimingBeam() 
        self.player.lazer_beam = LazerBeam() 
        floor_configuration["objects"].append( self.player.aiming_beam )
        floor_configuration["objects"].append( self.player.lazer_beam )
        self.aiming_beam = self.player.aiming_beam

        #self.light_occluders = self.generator.get_light_occluders()
        #self.physics_occluders = self.generator.get_physics_occluders()

        #self.photon_emitters = self.generator.get_photon_emitters()

        #self.light_occluders = []#self.generator.get_light_occluders()
        #self.photon_emitters = []#self.generator.get_photon_emitters()



        self.fog_level_real = 0.0
        self.fog_level_impulse = 0.0
        Floor.__init__(self,**floor_configuration)

    def reattach_player(self):
        self.player.aiming_beam = self.aiming_beam

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
            min_dist = 40
            portal = self.area.portals[idx]
            if portal.left_area is self.area:
                #portal_p = portal.left_p
                portal_target = portal.right_area
            elif portal.right_area is self.area:
                #portal_p = portal.right_p
                portal_target = portal.left_area


            tx = uniform(-self.width,self.width)*0.5
            ty = uniform(-self.height,self.height)*0.5
           
            valid = True
            for obj in objs:
                if hypot( tx-obj.p[0], ty-obj.p[1])<min_dist: 
                    valid = False
                    break
            if not valid:
                continue
            portal_object = Portal( p = [tx,ty], portal_target = portal_target )
            objs.append(portal_object)
            idx = idx + 1
 
        return objs

    def get_dynamic_light_occluders(self):
        occs = []
        for door in self.doors:
            occs.extend(door.get_light_occluders())
        return occs

    def add_fog(self,emitter, amt):

        dx =  emitter.p[0] - self.camera.p[0]
        dy =  emitter.p[1] - self.camera.p[1]
        md = (dx*dx)+(dy*dy)

        if md < 250:
            self.fog_level_impulse = self.fog_level_impulse + amt

    def tick(self):
        #dungeon floor

        self.fog_level_impulse = 0.0
        geometry = self.get_light_occluders()[:]
        geometry.extend( self.get_dynamic_light_occluders())

        self.vision_lightmap.update( geometry )
        self.dynamic_lightmap.update( geometry )
        if not KTState.paused:
            if(self.player.snap_animation_buffer<=0):
                Floor.tick(self)
            else:
                for tickable in self.purging_tick_manager.tickables:
                    if tickable.physics is None:
                        r = tickable.tick()
                        if not r:
                            self.purging_tick_manager.tickables.remove(tickable)
                        
                self.fog_level_impulse = -0.2
                self._tick = self._tick+0.25
            self.player.kill_success = False
        else:
            pass

        if(self.fog_level_impulse < self.fog_level_real):
            self.fog_level_real = (self.fog_level_real * 0.97) + (self.fog_level_impulse*0.03)
        if(self.fog_level_impulse > self.fog_level_real):
            self.fog_level_real = (self.fog_level_real * 0.95) + (self.fog_level_impulse*0.05)

    def get_occluders(self):
        return self.light_occluders

    def get_photon_emitters(self):
        return self.photon_emitters

    def get_physics_occluders(self):
        return self.physics_occluders

    def get_light_occluders(self):
        return self.light_occluders

