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
from .LevelProps.ShipExterior import ShipExterior
from .LevelProps.SpeechBubble import SpeechBubble
from .LevelProps.Telekine import Telekine
from .LevelProps.Prop import Prop
from .Pickups.HealthVial import HealthVial
from .Pickups.SoftwarePickup import SoftwarePickup
from .Pickups.SwordPickup import SwordPickup
from .Lights.FactoryLight import FactoryLight
from .Destructables.Crystal import Crystal
from .Destructables.Slime import Slime
from .Interaction.Door import Door
from .NPC.Elder import Elder
from .Decorators.TreeTop import TreeTop
from .Decorators.TreeRoots import TreeRoots
from .Decorators.TreeShadow import TreeShadow

class FTerm(Object):
    def parse(od,df):
        ret = []
        ret.append(FTerm(p=[od["x"],od["y"]]))
        ret.append(FTermStand(p=[od["x"],od["y"]]))
        ret.append(Terminal(title="Teleport to Ship", p=[od["x"],od["y"]]))
        return ret

    textures = [
        BGL.assets.get('KT-forest/texture/term0000'),
        BGL.assets.get('KT-forest/texture/term0001')
    ]

    def __init__(self,**kwargs):
        Object.__init__(self,**kwargs)
        self.buftarget = "floor"
        self.z_index = 2
        self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
        self.light_color = [ 0.8,0.0,1.0,1.0 ]
        self.light_radius = 25
        self.tick_type = Object.TickTypes.TICK_FOREVER
        self.size = [2.0,2.0]
        self.fr = 0 

    def tick(self):
        self.fr += 1
        if(self.fr==90):
            self.fr = 0
        self.texture = FTerm.textures[ int(self.fr)//45 ]

class FTermStand(Object):

    texture = BGL.assets.get('KT-forest/texture/termstand')

    def __init__(self,**kwargs):
        Object.__init__(self,**kwargs)
        self.p[1] += 1.5
        self.size = [3.0,3.0]
        self.buftarget = "floor"
        self.texture = FTermStand.texture
        self.tick_type = Object.TickTypes.STATIC
        self.physics = { "radius" : 1.2, "mass"   : 900, "friction" : 0.3 }

class BTerm(Object):
    def parse(od,df):
        ret = []
        ret.append(FTerm(p=[od["x"],od["y"]]))
        ret.append(FTermStand(p=[od["x"],od["y"]]))
        ret.append(Terminal(title="Commence Birth", p=[od["x"],od["y"]]))
        return ret

class Terminal(Object):
    def parse(od,df):
        return Terminal( title=od['meta']['title'], p = [ od['x'], od['y'] ] )

    def get_ui(self):
        return self.ui

    def customize(self):
        self.visible = False
        self.tick_type = Object.TickTypes.TICK_FOREVER

        self.install_percent = 0

        if self.title == "Commence Birth":
            self.ui = CommenceBirth(self)
            self.term_installed = True
            self.install_percent = 100
        elif self.title == "Teleport to Ship":
            self.ui = ReturnToShip(self)
            self.term_installed = True
            self.install_percent = 100
        elif self.title == "Teleport Control":
            self.ui = TeleportControl(self)
            self.term_installed = True
            self.install_percent = 100
        elif self.title == "Telekine Biometrics":
            self.ui = TelekineControl(self)
            self.term_installed = Abilities.InstallTelekine
            self.install_percent = 0
            if Abilities.TelekineInstalled:
                self.install_percent = 100
        elif self.title == "Sword Technology":
            self.ui = SwordControl(self)
            self.term_installed = False
            self.install_percent = 0
        else:
            self.ui = ShipComputer(self)
            self.term_installed = Abilities.InstallCentral
            self.install_percent = 0
            if Abilities.CentralInstalled:
                self.install_percent = 100

    def render_ui(self):
        self.ui.render()

    def tick(self):
        if(self.mdist(self.floor.player)<6.5): 

            if(self.install_percent<100) and self.term_installed:
                self.install_percent += choice([0.1,0.5,0.25])
                if self.install_percent >= 100:
                    if self.title == "Telekine Biometrics":
                        Abilities.Telekine = True
                        Telekine.instance.enable()
                    if self.title == "Central Processing":
                        Abilities.CentralInstalled = True
            if(self.floor.player.active_terminal != self):
                self.floor.player.active_terminal = self
                self.ui.setup_options()
                #self.floor.player.add_dm_message("You opened the {0} terminal".format(self.title))
                KSounds.play(KSounds.terminal_open)
        else:
            if self.floor.player.active_terminal == self:
                KSounds.play(KSounds.terminal_close)
                self.floor.player.active_terminal = None
                print("HIDING",self)

        
class SkullDeath(Object):
    texture = BGL.assets.get('KT-forest/texture/skull0000')

    def customize(self):
        self.texture = SkullDeath.texture
        self.buftarget = "hud"

        self.size =  [ 3.0, 3.0 ]
        self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
        self.light_color =  [ 1.0,0.0,1.0,1.0]
        self.color = [ 1.0,1.0,1.0,0.5]
        self.light_radius = 50.0
        self.physics = None
        self.z_index = 9000
        self.tick_type = Object.TickTypes.PURGING
        self.delta_vy = -0.03
        self.lifetime = 0
        self.delay = 0
        self.visible = False
        self.anim_tick = 0.2

    def tick(self):

        if(self.delay> 5):
            self.visible = True
            self.lifetime = self.lifetime + 1
            self.p[1] = self.p[1] + self.delta_vy
            self.delta_vy *= 1.1

            self.anim_tick = self.anim_tick * 1.08
            self.size[0] = sin( self.anim_tick ) * 5.0
            self.size[1] = self.size[1] * 1.02
            if(self.lifetime > 100):
                self.floor.objects.remove(self)
                return False
            return True
        else:
            self.delay = self.delay + 1
            return True

class ForestGraveyard():
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
        self.objects.append(SpeechBubble.instance)
        for pd in ad["prop_defs"]:
            self.objects.append( Prop.parse(pd) )

        for od in ad["object_defs"]:
            if od["key"] == "totem":
                self.objects.append(Totem( p = [ od['x'],od['y'] ]))
                df.snap_enemies.append(self.objects[-1])
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

            if od["key"] in [ "ship_exterior" ]:
                self.objects.append(ShipExterior.parse(od,df ))

            if od["key"] in [ "wormfield" ]:
                self.objects.append(WormField.parse(od,df ))

            if od["key"] in [ "telekine" ]:
                self.objects.append(Telekine.parse(od,df ))

            if od["key"] in [ "snap_enemy", "skeline"]:
                self.objects.append(Skeline.parse(od,df ))

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
    
            self.generate_inner_trees(dungeon_floor)
            self.generate_edge_trees()
            self.generate_tiledata(  dungeon_floor )



    def generate_fires(self,df):
        for pobj in filter( lambda x: "portal_target" in x.__dict__, self.objects):
            self.objects.append( Fire( p=pobj.p) )


    def generate_inner_trees(self,df):

        self.tree_pts = []
        occluders = []
        trees = 0

        for t in range(0,trees):
            px,py = uniform(-df.width,df.width),uniform(-df.height,df.height)
            px*=0.4
            py*=0.4
            rad = uniform(3.2,6.3)
            occluders.extend( self.gen_rand_circle_lines( 0.5,1.5, rad, [px,py]))

            size = uniform(1.0,8.0)
            plx = uniform(2.2,3.8)

            self.tree_pts.append([px,py])
            pobjs = filter( lambda x: "portal_target" in x.__dict__, self.objects)
            for tt in range(2,choice(range(4,5))):
                valid = False
                while not valid:
                    valid = True
                    min_dist = 25
                    p = [px+uniform(-3.0,3.0),py+uniform(-3.0,3.0)]
                    for obj in pobjs:
                        if hypot( p[0]-obj.p[0], p[1]-obj.p[1])<min_dist: 
                            valid = False
                            break

                tt = TreeTop( p=p, size=[size,size],parralax = plx) 
                self.objects.append( tt )
                #tt.visible = False
                self.objects.append( TreeShadow(p=p, TreeTop=tt) )
                size = size * uniform(1.2,1.5)
                plx = plx * uniform(1.1,1.3)
                size = uniform(3.0,7.0)
                self.objects.append( TreeRoots( p=p, size=[size,size]) )

            for tt in range(2,choice(range(2,5))):
                size = uniform(10.0,40.0)
                p = [px+uniform(-2.0,2.0),py+uniform(-2.0,2.0)]
                self.objects.append( TreeRoots( p=p, size=[size,size]) )
            #    if(choice([True,False])):
            #        self.objects.append( TreeShadow( p=p, size=[size*2,size*2]) )


            ##for tt in range(2,choice(range(3,15))):
            ##    p = [px+uniform(-3.0,3.0),py+uniform(-3.0,3.0)]
            ##    self.objects.append( TreeTop( p=p, size=[size,size],parralax = plx) )
            ##    size = size * uniform(1.2,1.5)
            ##    plx = plx * uniform(1.2,1.5)

        self.light_occluders.extend(occluders)


    def generate_edge_trees(self, edges = None):
        if "map_edges" in self.__dict__:
            if not edges:
                edges = self.map_edges 
        else:
            if not edges:
                edges = []

        for edge in edges:

            u_l = hypot( edge[1][0]-edge[0][0], edge[1][1]-edge[1][1])

            for x in range(0,int(u_l+uniform(0.0,5.0))):

                if uniform(0.0,1.0) < 0.85:
                    continue
                    
                size = uniform(2.5,5.5)
                dx = edge[1][0] - edge[0][0]
                dy = edge[1][1] - edge[0][1]
                d = uniform(0.0,1.0)
                px,py = d*dx,d*dy
                x,y = edge[0][0]+px,edge[0][1]+py
                p = [x,y]
                if(uniform(0.0,1.0)>0.2):
                    self.tree_pts.append(p)

                tt = TreeTop( p=p, size=[size,size],parralax = uniform(1.1,2.8)) 
                self.objects.append( tt )
                if(uniform(0.0,1.0)>0.8):
                    self.objects.append( TreeShadow(p=p, TreeTop=tt) )

                #for tt in range(2,choice(range(2,5))):
                #    size = uniform(10.0,40.0)
                #    p = [px+uniform(-2.0,2.0),py+uniform(-2.0,2.0)]
                #    self.objects.append( TreeRoots( p=p, size=[size,size]) )




    def get_objects(self):
        return self.objects


    def gen_rand_circle_lines(self,min_step,max_step,rad, p=[0.0,0.0]):
        r = -pi
        points = []
        dfilt = None
        while(r < pi):
            r = r + uniform(min_step,max_step)
            #rad = min(df.width,df.height)*0.5
            d = uniform(0.5*rad, 1.0*rad)
            if dfilt is None:
                dfilt = d
            else:
                dfilt = (d*0.2)+(dfilt*0.8)
            points.append( [ (cos(r)*dfilt)+p[0], (sin(r)*dfilt)+p[1] ] )


        lines = []
        for i in range(0, len(points)-1):
            lines.append( [ points[i],points[i+1]] )

        lines.append( [ points[len(points)-1],points[0]] )
        return lines

    def get_light_occluders(self):
        return self.light_occluders

    def get_tiledata(self):
        return self.tile_data

    def get_photon_emitters(self):
        return self.photon_emitters

    def generate_tiledata( self, df ):
        self.df = df 
        tile_data = [0]*(df.tilemap_width*df.tilemap_height)
        for tile_def in self.ad["tile_defs"]:
            addr = tile_def["x"] + (tile_def["y"]*df.tilemap_width)
            tile_data[addr] = tile_def["idx"] + 1
        self.tile_data = tile_data;
        return;

