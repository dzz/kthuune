####
#
# The Evil Emperor ZORDIUS has unleashed his army of CEPHLAPOADS on to the Bubble Worlds of
# KTHUNIA. They have taken the LIMIT BABIES - emobodiments of pure potential - hostage.

#
# Only VECTORLORD can stop the corruption, so YOU can get back to physics class
#
# YOU are the messiah. Do your job, QUICKLY.
#

import audio
from Beagle import API as BGL
from Newfoundland.Floor import createFloorClass
from Newfoundland.Tilemap import Tilemap
from Newfoundland.Object import Object
from random import choice
from .Universe.AreaCompiler import AreaCompiler
from .Universe.LevelProps.SpeechBubble import ToolTip
from .Renderers.DFRenderer import DFRenderer
from random import uniform
from math import sin,cos,hypot
#from .AimingBeam import AimingBeam
#from .AimingBeam import LazerBeam
from .KTState import KTState
from .KSounds import KSounds
import client.system.keyboard as keyboard

Floor = createFloorClass( DFRenderer )
class DungeonFloor( Floor ):

    current_music = None
    NO_SHADOWS = True #it's all caps coz its a hax

    def create_tickable(self,tickable):
        Floor.create_tickable(self,tickable)
 
    def playing_genocide(self):
        return self.game_mode == 1

    def add_timeout(self, to):
        self.timeouts.append(to)

    def __init__(self,**kwargs):
        BGL.auto_configurable.__init__(self,
        {
            "trigger_callbacks" : {},
            "spawners" : [],
            "forced_progression" : None,
            "forced_offset" : None,
            "genocide_enabled" : True,
            "CustomBackground" : None,
            "level_started" : False,
            "music" : None,
            "group_to_owl" : {},
            "renderable_tooltips" : [],
            "genocide_flash_timeout" : 60.0,
            "genocide_show_seconds" : 0.0,
            "_tick" : 0.0,
            "passed_genocide" : False,
            "activated_totem_groups" : [ 0 ],
            "game_mode" : 0,
            "totems" : [],
            "timeouts" : [],
            "chargeplates" : [],
            "hostages" : [],
            "override_base_zoom" : None,
            "custom_background" : None,
            "parallax_skin" : None,
            "blurring" : False,
            "fuzz_amt" : 0.0,
            "uses_vision" : True,
            "vision_mute" : 0.0,
            "vision_regions" : [],
            "active_vision_mute" : 0.0,
            "fade_vision_amt" : 0.0,
            "camera_lock_regions" : [],
            "title" : "Who Knows!",
            "god_shader" : None,
            "fog_level_base" : 0,
            "freeze_frames" : 0,
            "freeze_delay" : 0,
            "doors" : [],
            "snap_enemies" : [],
            "yellers" : [], # the bucket for yeller specific snap enemy lookups
            "suspended_enemies" : [],
            "enemies" : [],
            "using_tilemap" : True,
            "tilescale" : 3,
            "area_def" : None,
            "width" : 32,
            "height" : 32,
            "generator" : AreaCompiler(),
            "area" : None,
            "renderer_config" : {
                "vision_lightmap_width" : 1920,
                "vision_lightmap_height" : 1080,
                "photon_map_width" : 1024,
                "photon_map_height" : 1024,
                "static_lightmap_width" : 1024,
                "static_lightmap_height" : 1024,
                "dynamic_lightmap_width" : 1920,
                "dynamic_lightmap_height" : 1080,
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
                "tileheight" : 64,
                "tilewidth" : 64
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


        self.sounds = KSounds
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

        beagle_tilemap_fg = BGL.tilemap(
            tileset = beagle_tileset,
            configuration = {
                "layers" : [
                    {
                        "data" : self.generator.get_tiledata_fg(),
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
            "tilemap_fg" : Tilemap( tilescale = self.tilescale, beagle_tilemap = beagle_tilemap_fg, channel_textures = {
                "height" : BGL.assets.get("KT-tiles/texture/plain_tiles"),
                "reflection" : BGL.assets.get("KT-tiles/texture/plain_tiles")
            } ),
            "objects" : self.generator.get_objects(),
            "renderer_config" : self.renderer_config,
            "light_occluders" : self.generator.get_light_occluders(),
            "physics_occluders" : self.generator.get_physics_occluders(),
            "photon_emitters" :  self.generator.get_photon_emitters()
        })

       
        #self.player.aiming_beam = AimingBeam() 
        #self.player.lazer_beam = LazerBeam() 
        #floor_configuration["objects"].append( self.player.aiming_beam )
        #floor_configuration["objects"].append( self.player.lazer_beam )
        #self.aiming_beam = self.player.aiming_beam

        #self.light_occluders = self.generator.get_light_occluders()
        #self.physics_occluders = self.generator.get_physics_occluders()

        #self.photon_emitters = self.generator.get_photon_emitters()

        #self.light_occluders = []#self.generator.get_light_occluders()
        #self.photon_emitters = []#self.generator.get_photon_emitters()

        self.fog_level_real = 0.0
        self.fog_level_impulse = 0.0
        self.sound_tick = 0
        self.recursive_snapper = None
        self.destroyed = False
        Floor.__init__(self,**floor_configuration)

        self.tilemap_fg.linkFloor(self)
        self.active_vision_mute = self.vision_mute

    def destroy(self):
        self.game.tickables.remove(self)
        self.game.floor = None
        self.game = None
        for obj in self.objects:
            if "body" in obj.__dict__:
                if(obj.body):
                    obj.body.destroy()
                    obj.body = None
                    obj.floor = None

        self.objects = []
        self.physics_space.destroy()
        self.physics_space = None
        self.player.floor = None
        self.player.hittable_hilight = []
        self.camera = None
        self.player = None
        self.destroyed = True

    def tick_god_shader(self):
        pass

    def reattach_player(self):
        pass
        #self.player.aiming_beam = self.aiming_beam

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

    def synch_tooltips(self):
        tooltip_garbage = []
        newtooltips = []
        width = 20

        for obj in self.objects:
            if "tooltip" in obj.__dict__:
                if not ("_tooltip" in obj.__dict__):
                    obj._tooltip = None
                if obj._tooltip in self.renderable_tooltips:
                    if(obj.tooltip != obj._tooltip.message):
                        tooltip_garbage.append(obj._tooltip) #garbage the old tooltip
                        if obj.tooltip is not None:
                            tt = ToolTip( floor=self,owner=obj, p = obj.p, message=obj.tooltip, width=width)
                            obj._tooltip = tt
                            newtooltips.append(tt)
                else:
                    if obj.tooltip is not None:
                        tt = ToolTip( floor=self,owner=obj, p = obj.p, message=obj.tooltip, width=width)
                        obj._tooltip = tt
                        newtooltips.append(tt)
            
        self.renderable_tooltips = [tt for tt in self.renderable_tooltips if tt not in tooltip_garbage and tt.owner in self.objects]
        self.renderable_tooltips.extend(newtooltips)



    def tick(self):
        if self.CustomBackground:
            CustomBackground.tick()

        if not self.level_started:
            self.sounds.play(self.sounds.level_start)
            self.level_started = True

        if DungeonFloor.current_music is not self.music:
            DungeonFloor.current_music = self.music
            #audio.baudy_play_music(BGL.assets.get(self.music))

        if DungeonFloor.NO_SHADOWS:
            self.light_occluders = []

        self.synch_tooltips()
        #def make_follower(enemy):
        #    def h():
        #        enemy.floor.camera.grab_cinematic( enemy, 30 )
        #    return h


        if(self.forced_progression):
            self.handle_forced_progression()

        if(self.playing_genocide()):
            self.genocide_flash_timeout -= 1
            if(self.genocide_flash_timeout<0):
                self.genocide_flash_timeout = 60
                self.genocide_show_seconds += 1
                for enemy in self.enemies:
                    enemy.flash_color = [ 1.0,1.0,1.0,1.0 ]

                #if self.genocide_show_seconds > 5:
                #    self.genocide_show_seconds = 0
                #    for i,enemy in enumerate(self.enemies):
                #        self.add_timeout( [ make_follower(enemy), i*30 ] )
                        
                    


        self._tick = self._tick + 0.01
        pX = self.player.p[0]
        pY = self.player.p[1]
        target_vision_mute = self.vision_mute
        for region in self.vision_regions:
            if pX > region[0] and pX < region[2] and pY > region[1] and pY < region[3]:
                target_vision_mute = 0.0
                break

        self.active_vision_mute = (self.active_vision_mute * 0.9) + (target_vision_mute*0.1)

        #dungeon floor

        if(self.sound_tick==0):
            KSounds.play(choice([KSounds.rain_20sec, KSounds.rain_21sec]))
        self.sound_tick = (self.sound_tick +1)%(60*18)

        self.fog_level_impulse = 0.0
        geometry = self.get_light_occluders()[:]
        #geometry.extend( self.get_dynamic_light_occluders())

        #self.vision_lightmap.update( geometry )
        self.dynamic_lightmap.update( geometry )
        if not KTState.paused:
            if(self.player.snap_animation_buffer<=0) or (self.player.snap_animation_buffer%5==0):
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

        #timeouts
        done_to = []
        for to in self.timeouts:
            to[1]-=1
            if to[1] == 0:
                to[0]()
                done_to.append(to)

        for to in done_to: 
            self.timeouts.remove(to) 

            

    def get_occluders(self):
        return self.light_occluders

    def get_photon_emitters(self):
        return self.photon_emitters

    def get_physics_occluders(self):
        return self.physics_occluders

    def get_light_occluders(self):
        return self.light_occluders

    def get_owl_p(self,idx = 0 ):
        if not idx in self.group_to_owl:
            return ( 0.0,0.0 )        
        else:
            return self.group_to_owl[idx].p

    def get_owl(self,idx = 0 ):
        if not idx in self.group_to_owl:
            return None
        else:
            return self.group_to_owl[idx]

    def start_forced_progression(self,vx,vy):
        self.forced_progression = (vx,vy)
        self.forced_offset = [ self.player.p[0], self.player.p[1] ]

    def end_forced_progression(self):
        self.forced_offset = None
        self.forced_progression = None

    def get_forced_offset(self):
        return self.forced_offset
    
    def handle_forced_progression(self):
        self.forced_offset[0] += self.forced_progression[0]
        self.forced_offset[1] += self.forced_progression[1]

def get_DF():
    return DungeonFloor
