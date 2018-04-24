#### MACHINE GIRL 
#### BATMAN 
#### ZELDA
#### STIMULANTS
#### PAGANISM
#### BREAKCORE TEMPOS
#### SIEZURES
#### DARK SOULS
#### X FILES

import gc
from random import uniform, choice
from math import hypot
from Newfoundland.Object import Object
from Beagle import API as BGL
from math import sin,cos,pi
from .txt_specs import *
from math import atan2
from .SVGLoader import get_level_data
from math import floor
from .magic_lines import vscan_line, fill_scanline
import random
from client.beagle.Newfoundland.GeometryUtils import segments_intersect
from .ShipComputer import ShipComputer, TeleportControl, TelekineControl, SwordControl, ReturnToShip, CommenceBirth

from ..KSounds import KSounds
from ..KPlayer import Sword
from ..GeneratorOptions import GeneratorOptions
from ..Abilities import Abilities

from .Hazards.WormField import WormField
from .Hazards.Firepot import Firepot
from .Enemies.SnapEnemy import SnapEnemy
from .Enemies.Acolyte import Acolyte
from .Enemies.Skeline import Skeline
from .Enemies.Stork import Stork
from .Enemies.TumorCrab import TumorCrab
from .Enemies.Cleric import Cleric
from .Enemies.EglanBlob import EglanBlob
from .Particles.SplatterParticle import SplatterParticle
from .Particles.CrystalChunk import CrystalChunk
from .LevelEffects.Blood import Blood
from .LevelEffects.SpikeyWave import SpikeyWave
from .LevelEffects.ChromaticWave import ChromaticWave
from .Locomotion.Totem import Totem
from .Locomotion.OnewayFadeSwitch import OnewayFadeSwitch
from .RangedEnemyAttacks.BasicProjectile import BasicProjectile        
from .Configuration.vconf import vconf
from .LevelProps.Egg import Egg
from .LevelProps.FloatingPlayer import FloatingPlayer
from .LevelProps.DeadK import DeadK
from .LevelProps.Lantern import Lantern
from .LevelProps.ShipExterior import ShipExterior
from .LevelProps.SpeechBubble import SpeechBubble
from .LevelProps.Telekine import Telekine
from .LevelProps.Prop import Prop
from .LevelProps.Stainglass import Stainglass
from .LevelProps.CableSegment import CableSegment
from .Pickups.HealthVial import HealthVial
from .Pickups.SoftwarePickup import SoftwarePickup
from .Pickups.SwordPickup import SwordPickup
from .Lights.FactoryLight import FactoryLight
from .Destructables.Crystal import Crystal
from .Destructables.Slime import Slime
from .Interaction.Door import Door
from .NPC.Elder import Elder
from .NPC.Hostage import Hostage
from .Interaction.Chargeplate import Chargeplate
from .Decorators.TreeTop import TreeTop
from .Decorators.TreeRoots import TreeRoots
from .Decorators.TreeShadow import TreeShadow
from .Interaction.Terminals import *

class AreaCompiler():
    def __init__(self):
        pass

    def get_physics_occluders(self):
        return self.physics_occluders

    def process_area_def( self, df, ad ):

        SpeechBubble.instance = SpeechBubble()
        self.tree_pts = [ [-10,-10] ]
        self.guider_pts = [ [10,10] ]
        ######################################
        self.df = df

        player_start = list(filter(lambda x: x["key"] == 'player_start', ad["object_defs"]))[0]
        df.player.p[0] = player_start['x']
        df.player.p[1] = player_start['y']


        self.door_pins = {}
        self.door_ends = {}
        self.door_sensors = {}

        self.objects = []

        #self.light_occluders = []
        self.light_occluders = ad["light_occluders"]
        self.physics_occluders = ad["physics_occluders"]
        self.decorators = ad["decorators"]
        self.photon_emitters = []

        self.generate_edge_trees( self.decorators )

        self.magic_lines = ad["magic_lines"]
        self.ad = ad
        self.generate_tiledata(df)
        df.area_switches = []

        self.objects.extend( CableSegment.generate_cable(-30.0,0.0,30.0,0.0) )
        self.objects.extend( CableSegment.generate_cable(0.0,-30.0,0.0,30.0) )
        self.objects.extend( CableSegment.generate_cable(30.0,30.0,-30.0,-30.0) )
        self.objects.extend( CableSegment.generate_cable(30.0,-30.0,-30.0,30.0) )

        self.objects.append(SpeechBubble.instance)
        for pd in ad["prop_defs"]:
            self.objects.append( Prop.parse(pd) )

        for od in ad["object_defs"]:
            if od["key"] == "totem":
                group = 0
                if "group" in od["meta"]:
                    group = od["meta"]["group"];    
                self.objects.append(Totem( group = group, p = [ od['x'],od['y'] ]))

                if(group!=0):
                    self.objects[-1].active = False
                    self.objects[-1].visible = False
                    self.objects[-1].reset_timer = Totem.reset_time
                else:
                    df.snap_enemies.append(self.objects[-1])
                df.totems.append(self.objects[-1])
                if "shield" in od["meta"]:
                    if od["meta"]["shield"]:
                        self.objects[-1].shield_totem = True
            if od["key"] == "light":
                self.objects.append(FactoryLight( factory_def = od ))
            if od["key"] == "door_pin":
                self.door_pins[od["meta"]["door"]] = od
            if od["key"] == "door_end":
                self.door_ends[od["meta"]["door"]] = od
            if od["key"] == "door_sensor":
                if not od["meta"]["door"] in self.door_sensors:
                    self.door_sensors[od["meta"]["door"]] = []
                self.door_sensors[od["meta"]["door"]].append(od)

            if od["key"] == "area_switch":
                p = [ od["x"], od["y"] ]
                target_area = od["meta"]["target_area"]
                target_switch = od["meta"]["target_switch"]
                switch_name = od["meta"]["name"]
                area_switch = AreaSwitch( switch_name = switch_name, p = p, target_area = target_area, target_switch = target_switch)
                df.area_switches.append(area_switch)
                self.objects.append(area_switch)
                

            if od["key"] == "gate_photon":
                for i in range(0,8):
                    emitter_def = [ od["x"]-5.0,od["y"]-5.0, 10.0,10.0, [ 0.8,0.4,1.0,1.0] ]    
                    self.photon_emitters.append(emitter_def)

            if od["key"] == "friend_photon":
                for i in range(0,8):
                    emitter_def = [ od["x"]-5.0,od["y"]-5.0, 10.0,10.0, [ 0.3,0.5,1.0,1.0] ]    
                    self.photon_emitters.append(emitter_def)

            if od["key"] == "orange_photon":
                for i in range(0,8):
                    emitter_def = [ od["x"]-5.0,od["y"]-5.0, 10.0,10.0, [ 1.0,0.9,0.3,1.0] ]    
                    self.photon_emitters.append(emitter_def)

            if od["key"] == "next_forest_photon":
                for i in range(0,8):
                    emitter_def = [ od["x"]-5.0,od["y"]-5.0, 10.0,10.0, [ 0.3,1.0,0.5,1.0] ]    
                    self.photon_emitters.append(emitter_def)

            if od["key"] in [ "oneway_fade_switch"]:
                self.objects.append(OnewayFadeSwitch.parse(od,df))
                
            if od["key"] in [ "egg" ]:
                if not Abilities.Born:
                    self.objects.append(Egg.parse(od,df ))
                    self.objects.append(FloatingPlayer.parse(od,df ))

            if od["key"] in [ "deadk1" ]:
                for x in range(0,16):
                    bloodp = [ od["x"]+uniform(-4.0,2.0), od["y"]+uniform(-1.0,2.5) ]
                    self.objects.append(Blood( p = bloodp))
                    
                self.objects.append(DeadK.parse(od,df ))

            if od["key"] in [ "lantern" ]:
                self.objects.append(Lantern.parse(od,df ))

            if od["key"] in [ "ship_exterior" ]:
                self.objects.append(ShipExterior.parse(od,df ))

            if od["key"] in [ "wormfield" ]:
                self.objects.append(WormField.parse(od,df ))

            if od["key"] in [ "telekine" ]:
                self.objects.append(Telekine.parse(od,df ))

            if od["key"] in [ "snap_enemy", "skeline"]:
                self.objects.append(Skeline.parse(od,df ))

            if od["key"] in [ "hostage" ]:
                self.objects.append(Hostage.parse(od,df ))

            if od["key"] in [ "stainglass" ]:
                self.objects.append(Stainglass.parse(od,df ))

            if od["key"] in [ "chargeplate" ]:
                self.objects.append(Chargeplate.parse(od,df ))
                df.chargeplates.append(self.objects[-1])
                self.objects.extend( self.objects[-1].generate_cable(df) )

            if od["key"] in [ "eglans" ]:
                for x in range(0,5):
                    self.objects.append(EglanBlob.parse(od,df ))

            if od["key"] in [ "cleric"]:
                self.objects.append(Cleric.parse(od,df ))

            if od["key"] in [ "acolyte" ]:
                self.objects.append(Acolyte.parse(od,df ))

            if od["key"] in [ "stork" ]:
                self.objects.append(Stork.parse(od,df ))
            
            if od["key"] in ["elder" ]:
                self.objects.append(Elder.parse(od,df))

            if od["key"] in ["tumorcrab"]:
                self.objects.append(TumorCrab.parse(od,df))

            if od["key"] in ["software" ]:
                if od["meta"]["key"] == "telekine": 
                    if not Abilities.InstallTelekine:
                        self.objects.append(SoftwarePickup.parse(od,df))
                    else:
                        for x in range(0,3):
                            self.objects.append(Skeline.parse(od,df))
                elif od["meta"]["key"] == "central": 
                    if not Abilities.InstallCentral:
                        self.objects.append(SoftwarePickup.parse(od,df))
                    else:
                        for x in range(0,2):
                            self.objects.append(Skeline.parse(od,df))

                else:
                    self.objects.append(SoftwarePickup.parse(od,df))

            if od["key"] in ["sword_pickup" ]:
                if not Abilities.Sword:
                    self.objects.append(SwordPickup.parse(od,df))
                else:
                    for x in range(0,3):
                        self.objects.append(Skeline.parse(od,df))


            if od["key"] in ["firepot", "firepot_right" ]:
                self.objects.append(Firepot.parse(od,df))

            if od["key"] in ["firepot_up" ]:
                fp = Firepot.parse(od,df)
                fp.fire_rad = -3.14/2
                self.objects.append(fp)

            if od["key"] in ["firepot_down" ]:
                fp = Firepot.parse(od,df)
                fp.fire_rad = 3.14/2
                self.objects.append(fp)

            if od["key"] in ["firepot_left" ]:
                fp = Firepot.parse(od,df)
                fp.fire_rad = 3.14
                self.objects.append(fp)

            if od["key"] in ["crystals" ]:
                cs = Crystal.parse(od,df)
                self.objects.extend(cs)

            if od["key"] in ["slimes" ]:
                cs = Slime.parse(od,df)
                self.objects.extend(cs)

            if od["key"] in ["text" ]:
                self.objects.append(SpeechBubble.parse(od,df))


            if od["key"] in ["camlock_x", "camlock_y", "camlock" ]:
                if( od["key"] == "camlock_x" ):
                    axes = 0
                if( od["key"] == "camlock_y" ):
                    axes = 1
                if( od["key"] == "camlock" ):
                    axes = 2
                zoom = -1
                if "zoom" in od["meta"]:
                    zoom = float(od["meta"]["zoom"])
                lock_region = ( od["x"], od["y"], od["x"]+od["w"], od["y"]+od["h"], axes, zoom )
                df.camera_lock_regions.append( lock_region )

            if od["key"] in ["vision_region"]:
                vision_region = ( od["x"], od["y"], od["x"]+od["w"], od["y"]+od["h"] )
                df.vision_regions.append( vision_region )
                

            if od["key"] in ["terminal"]:
                self.objects.append(Terminal.parse(od,df))

            if od["key"] in ["fterm"]:
                self.objects.extend(FTerm.parse(od,df))

            if od["key"] in ["bterm"]:
                self.objects.extend(BTerm.parse(od,df))




    def link_doors(self):
        for key in self.door_sensors:
            self.objects.append( Door( door_pin = self.door_pins[key], door_end = self.door_ends[key], sensors = self.door_sensors[key] ) )            
            self.df.doors.append( self.objects[-1] )

    def compile(self, dungeon_floor, base_objects ):

        if dungeon_floor.area_def:
            self.process_area_def( dungeon_floor, dungeon_floor.area_def )
            self.link_doors()
            if len(dungeon_floor.chargeplates)==0:
                dungeon_floor.game_mode = Chargeplate.GENOCIDE

        elif dungeon_floor.area_def is None:
            self.objects = []
            if(base_objects):
                self.objects.extend(base_objects)
    
    
            self.generate_sigil_points( dungeon_floor )
            self.light_occluders = []
            self.guider_pts = []
            self.guiders = level_data["all_guiders"]
            self.make_guider_photons(dungeon_floor)
            self.map_edges = level_data["all_lines"]
            dungeon_floor.player.p[0] = level_data["player_start"][0]
            dungeon_floor.player.p[1] = level_data["player_start"][1]
            self.df = dungeon_floor
    
            dungeon_floor.player.sword.p[0] = level_data["sword_start"][0]
            dungeon_floor.player.sword.p[1] = level_data["sword_start"][1]
            
            elder = Elder()
            elder.p = level_data["elder_start"]
    
            for wormfield in level_data["wormfields"]:
                self.objects.append( WormField( wf_spec=wormfield ) )
    
            for totem in level_data["totems"]:
                self.objects.append( Totem( p = totem ) )
    
            for skeline in level_data["skelines"]:
                self.objects.append( Skeline( p = skeline ) )
    
            self.objects.append( elder )
            self.light_occluders = []
            self.light_occluders.extend( self.map_edges )
    
            self.generate_edge_trees()
            self.generate_tiledata(  dungeon_floor )



    def generate_edge_trees(self, edges = None):
        if "map_edges" in self.__dict__:
            if not edges:
                edges = self.map_edges 
        else:
            if not edges:
                edges = []

        for edge in edges:

            u_l = hypot( edge[1][0]-edge[0][0], edge[1][1]-edge[1][1])

            for x in range(0,int(u_l+uniform(1.0,3.0))):

                if uniform(0.0,1.0) < 0.98:
                    continue
                    
                size = uniform(2.5,5.5)
                dx = edge[1][0] - edge[0][0]
                dy = edge[1][1] - edge[0][1]
                d = uniform(0.0,1.0)
                px,py = d*dx,d*dy
                x,y = edge[0][0]+px,edge[0][1]+py
                p = [x,y]
                #if(uniform(0.0,1.0)>0.2):
                #    self.tree_pts.append(p)

                tt = TreeTop( p=p, size=[size,size],parralax = uniform(1.1,2.8)) 
                self.objects.append( tt )
                if(uniform(0.0,1.0)>0.5):
                    self.objects.append( TreeShadow(p=p, TreeTop=tt) )

                #for tt in range(1,choice(range(1,2))):
                #    size = uniform(10.0,40.0)
                #    p = [px+uniform(-2.0,2.0),py+uniform(-2.0,2.0)]
                #    self.objects.append( TreeRoots( p=p, size=[size,size]) )


    def get_objects(self):
        return self.objects

    def get_light_occluders(self):
        return self.light_occluders

    def get_tiledata(self):
        return self.tile_data

    def get_tiledata_fg(self):
        return self.tile_data_fg

    def get_photon_emitters(self):
        return self.photon_emitters

    def generate_tiledata( self, df ):
        self.df = df 
        tile_data = [0]*(df.tilemap_width*df.tilemap_height)
        tile_data_fg = [0]*(df.tilemap_width*df.tilemap_height)
        for tile_def in self.ad["tile_defs"]:
            addr = tile_def["x"] + (tile_def["y"]*df.tilemap_width)
            if not "layer" in tile_def:
                tile_data[addr] = tile_def["idx"] + 1
            else:
                tile_data_fg[addr] = tile_def["idx"] + 1

        self.tile_data = tile_data
        self.tile_data_fg = tile_data_fg
        return;

