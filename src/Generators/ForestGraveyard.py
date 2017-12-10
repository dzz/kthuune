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
from .Enemies.SnapEnemy import SnapEnemy
from .Enemies.Acolyte import Acolyte
from .Enemies.Skeline import Skeline
from .Enemies.Stork import Stork
from .Enemies.TumorCrab import TumorCrab
from .Enemies.Cleric import Cleric
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
from .Pickups.HealthVial import HealthVial
from .Pickups.SoftwarePickup import SoftwarePickup
from .Lights.FactoryLight import FactoryLight

class Breakable(Object):
    def handle_pull(self):
        dx = self.p[0] - self.floor.player.p[0]
        dy = self.p[1] - self.floor.player.p[1]
        self.floor.player.v[0] += dx * 2.2
        self.floor.player.v[1] += dy * 2.2

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


class Slime(Breakable):
    def parse(od,df):
        ret = []
        for x in range(0,3):
            o = Slime( rad = uniform(0.0,6.5), p = [ od["x"], od["y"] ] )
            ret.append(o)
        return ret

    textures = [
        BGL.assets.get('KT-forest/texture/slime0small'),
        BGL.assets.get('KT-forest/texture/slime0big'),
    ]

    def customize(self):
        self.tick_type = Object.TickTypes.PURGING
        self.buftarget = "popup"
        self.visible = True
        self.texture = choice ( Slime.textures )
        sz = uniform(5.0,9.0)
        self._sz = sz
        self.size = [ sz*2.7,sz*2.7 ]
        self.base_size = [ self.size[0], self.size[1] ]
        self.physics = { "radius" : sz/3, "mass"   : 900000, "friction" : 0.3 }
        self.hitFr = 0
        self.hp = 2
        self.fridx = 0.0
        self.offs = uniform(0.0,3.14)
        self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
        self.light_radius = 30
        self.light_color = [ -0.3,0.3,-0.3,1.0]

    def tick(self):
        self.fridx += 0.01
        self.size[0] = (self.base_size[0] + (sin(self.fridx+self.offs)*2.0))*0.4
        self.size[1] = (self.base_size[1] + (cos(self.fridx+self.offs*0.8)*2.0))*0.4
        if self.hp>0:
            self.texture = Slime.textures[self.hp-1]
        if(self.hitFr>0):
            self.hitFr-=1
            self.rad+=uniform(-0.02,0.02)

        d = self.mdist( self.floor.player )

        if d < 90:
            self.floor.add_fog(self, 20.0 )
        if(self.hitFr==0):
            if self.floor.player.slash.visible:
                if d < self._sz*1.2:
                    #self.floor.player.add_dm_message("You hit a crystal with your sword")
                    for x in range(0,5):
                        self.floor.create_object( SplatterParticle( size = [ 5.0,5.0], ptexture = Slime.textures[0], rad=uniform(0.0,6.5), p = [ self.p[0], self.p[1]]))
                    KSounds.play(KSounds.slimecrush)
                    KSounds.play(KSounds.slashhit)
                    self.hitFr = 30
                    self.hp-=1

        if(self.hp==0):
            KSounds.play(KSounds.slimekill)
            self.handle_pull()
            self.floor.remove_object(self)

            #self.floor.player.add_dm_message("You smashed a crystal with your sword")
            #if uniform(0.0,1.0)>0.78:
            #    self.floor.create_object(ResourcePickup(p=[ self.p[0], self.p[1]]))
            
            for x in range(0,3):
                self.floor.create_object(Blood(p=[self.p[0]+uniform(-3.0,3.0),self.p[1]+uniform(-3.0,3.0)]))
            for x in range(0,15):
                self.floor.create_object( SplatterParticle( size = [ 5.0,5.0], ptexture = Slime.textures[0], rad= uniform(0.0,6.5), p = [ self.p[0], self.p[1]]))
            return False
        return True

    def get_shader_params(self):
        bp = Object.get_shader_params(self)

        if self.hitFr > 0:
            bp['translation_local'][0] += uniform(-0.01,0.01)
            bp['filter_color'] = [ 10.0,10.0,10.0,1.0]
        return bp


class Crystal(Breakable):
    def parse(od,df):
        ret = []
        for x in range(0,3):
            o = Crystal( rad = uniform(0.0,6.5), p = [ od["x"], od["y"] ] )
            ret.append(o)
        return ret

    textures = [
        BGL.assets.get('KT-forest/texture/crystal_1'),
        BGL.assets.get('KT-forest/texture/crystal_2'),
        BGL.assets.get('KT-forest/texture/crystal_3'),
        BGL.assets.get('KT-forest/texture/crystal_4'),
        BGL.assets.get('KT-forest/texture/blocker1'),
        BGL.assets.get('KT-forest/texture/blocker2'),
    ]

    def customize(self):
        self.tick_type = Object.TickTypes.PURGING
        self.buftarget = "popup"
        self.visible = True
        self.texture = choice ( Crystal.textures )
        sz = uniform(4.0,8.0)
        self._sz = sz
        self.size = [ sz*0.7,sz*0.7 ]
        self.physics = { "radius" : sz/3, "mass"   : 900000, "friction" : 0.3 }
        self.hitFr = 0
        self.hp = choice([1,1,2])

    def tick(self):

        if(self.hitFr>0):
            self.hitFr-=1
            self.rad+=uniform(-0.02,0.02)

        if(self.hitFr==0):
            if self.floor.player.slash.visible:
                d = self.mdist( self.floor.player )
                if d < self._sz*1.2:
                    #self.floor.player.add_dm_message("You hit a crystal with your sword")
                    for x in range(0,5):
                        self.floor.create_object( CrystalChunk( p = [ self.p[0], self.p[1]]))
                    KSounds.play(KSounds.mining1)
                    self.hitFr = 30
                    self.hp-=1

        if(self.hp==0):
            KSounds.play(KSounds.mining2)
            self.handle_pull()
            self.floor.remove_object(self)

            #self.floor.player.add_dm_message("You smashed a crystal with your sword")
            if uniform(0.0,1.0)>0.78:
                self.floor.create_object(ResourcePickup(p=[ self.p[0], self.p[1]]))
            
            for x in range(0,15):
                self.floor.create_object( CrystalChunk( p = [ self.p[0], self.p[1]]))
            return False
        return True

    def get_shader_params(self):
        bp = Object.get_shader_params(self)

        if self.hitFr > 0:
            bp['translation_local'][0] += uniform(-0.2,0.2)
            bp['filter_color'] = [ 10.0,10.0,10.0,1.0]
        return bp


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
        




class SwordPickup(Object):
    textures = [ 
        BGL.assets.get("KT-player/texture/sword"),
    ]
   
    def parse(od,df):
        o = SwordPickup( p = [ od["x"], od["y"] ] )
        return o
        
    def customize(self):
        self.fridx = 0
        self.texture = SwordPickup.textures[0]
        self.buftarget = "popup"
        self.base_p = list(self.p)
        self.tick_type = Object.TickTypes.PURGING
        self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
        self.light_color = [ 0.0, 1.0, 1.0, 1.0 ]
        self.light_radius = 25.
        self.visible = True
        self.size = [ 2.5,2.5 ]
        self.rad = 3.14/2

    def tick(self):
        self.visible = True

        self.fridx = (self.fridx + 1) % 80
 
        y_offs = sin(self.fridx*(3.14/40.0))
        self.light_radius = 25. + y_offs

        self.size[1] = 2.5*y_offs
        self.p[1] = self.base_p[1] + (y_offs*0.15)

        dx = self.p[0] - self.floor.player.p[0]
        dy = self.p[1] - self.floor.player.p[1]

        md = (dx*dx) + (dy*dy)

        if (md<1.6):
            sb = SpeechBubble( p = list(self.floor.player.p) )
            sb.trigger_script = [ "HEY! BASTARD!", "PUSH (A) TO SLASH" ]
            sb.mode = 1
            self.floor.create_object( sb )
            self.floor.objects.remove(self)
            KSounds.play( KSounds.crit )
            self.floor.player.add_dm_message("You found a SWORD")

            self.floor.player.flash_color = [ 1.0,1.0,1.0,1.0]
            Abilities.Sword = True

            return False
        return True



            

class Door(Object):
    def customize(self):
        self.visible = False
        self.tick_type = Object.TickTypes.TICK_FOREVER
        self.parsed_pin = [ self.door_pin['x'], self.door_pin['y'] ]
        self.parsed_end = [ self.door_end['x'], self.door_end['y'] ]
        self.parsed_sensors = []
        for sensor in self.sensors:
            self.parsed_sensors.append([sensor['x'],sensor['y']])
        self.opening = False
        self.closed_ratio = 1.0
        self.effective_closed_ratio = 1.0
        self.sensrad2 = 30
        self.open_speed = 0.06
        self.close_speed = 0.1
    
    def tick(self):
        self.effective_closed_ratio = (self.effective_closed_ratio * 0.8) + (self.closed_ratio*0.2)
        self.opening = False
        for sensor in self.parsed_sensors:
            dx = self.floor.player.p[0] - sensor[0]
            dy = self.floor.player.p[1] - sensor[1]
            md = (dx*dx) + (dy*dy)
            if( md < self.sensrad2 ):
                self.opening = True
                break
        if self.opening:
            if self.closed_ratio > 0.0:
                self.closed_ratio = self.closed_ratio - self.open_speed                
        else:
            if self.closed_ratio < 1.0:
                self.closed_ratio = self.closed_ratio + self.close_speed

    def get_light_occluders(self):
        dx = (self.parsed_end[0] - self.parsed_pin[0]) * self.effective_closed_ratio
        dy = (self.parsed_end[1] - self.parsed_pin[1]) * self.effective_closed_ratio
       
        ex = dx + self.parsed_pin[0] 
        ey = dy + self.parsed_pin[1] 

        return [ [ self.parsed_pin, [ex,ey] ] ]
        

class Prop(Object):
    def parse(pd):
        p = Prop( texture = BGL.assets.get("KT-props/texture/" + pd["image"]))
        p.p[0] = pd["x"]
        p.p[1] = pd["y"]
        p.size[0] = pd["w"]
        p.size[1] = pd["h"]
        p.r = pd["r"]

        if "layer" in pd and pd["layer"]==0:
            p.z_index = -1000
            p.buftarget="underfloor"
        else:
            p.buftarget = "floor"
            p.z_index = 1

        return p

class Firepot(Object):
    textures = [
        BGL.assets.get("KT-forest/texture/firepot0000"),
        BGL.assets.get("KT-forest/texture/firepot0001"),
        BGL.assets.get("KT-forest/texture/firepot0002"),
        BGL.assets.get("KT-forest/texture/firepot0003"),
        BGL.assets.get("KT-forest/texture/firepot0004"),
        BGL.assets.get("KT-forest/texture/firepot0005"),
    ]

    def customize(self):
        self.z_index = 1
        self.buftarget = "popup"
        self.tick_type = Object.TickTypes.TICK_FOREVER
        self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
        self.light_color = [0.0,1.0,1.0,1.0]
        self.light_radius = 1.5
        self.texture = Firepot.textures[0]
        self._fr = (0 - floor((self.p[1]+self.p[0])*3))%60
        self.size = [2.0,2.0]
        self.fire_rad = 0

    def tick(self):
        self._fr = (self._fr +1)%60
        self.texture = Firepot.textures[self._fr//10]
        self.light_radius *= 1.02
        if(self._fr == 50):
            self.light_radius = 1.5
            bolt = BasicProjectile( p = [ self.p[0], self.p[1] ], rad = self.fire_rad ) 
            self.floor.create_object( bolt )
            bolt.lifespan = 40
            bolt.rad += uniform(-0.04,0.04)

    def parse(od,df):
        o = Firepot( p = [ od["x"], od["y"] ] )
        return o


        
class EglanBlob(SnapEnemy):

    def parse(od,df):
        eb = EglanBlob( p = [ od['x'],od['y'] ] )        
        df.snap_enemies.append(eb)
        return eb

    textures = [
        BGL.assets.get("KT-forest/texture/eglanblob1"),
        BGL.assets.get("KT-forest/texture/eglanblob2"),
        BGL.assets.get("KT-forest/texture/eglanblob3"),
        BGL.assets.get("KT-forest/texture/eglanblob4"),
        BGL.assets.get("KT-forest/texture/eglanblob5"),
        BGL.assets.get("KT-forest/texture/eglanblob6"),
        BGL.assets.get("KT-forest/texture/eglanblob7"),
    ] 

    def customize(self):
        self.snap_type = SnapEnemy.ENEMY
        self.triggered = False
        self.hp = 160
        self.dead = False
        self.tick_type = Object.TickTypes.PURGING
        self.physics = { "radius" : 0.5, "mass"   : 0.0003, "friction" : 1.0 }
        self.buftarget = "popup"
        self.visible = True
        self.texture = EglanBlob.textures[0]
        self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
        self.light_radius = 25
        self.defense = 1
        self.size = [ 7.0,7.0]
        self.iframes = 0
        self.fridx = uniform(0.0,100.0)
        self.snap_effect_emit = 0
        self.firing = False
        self.fire_idx = 0
        SnapEnemy.set_combat_vars(self)

    def fireRanged(self, rad):
        self.flash(1.0,0.8,0.0)
        #x = self.floor.player.p[0] - self.p[0]
        #y = self.floor.player.p[1] - self.p[1]
        #rad = atan2(y,x)
        self.floor.create_object( BasicProjectile( p = [ self.p[0], self.p[1] ], rad = rad ) )
        KSounds.play_eproj()

    def tick(self):
        self.fade_flash()
        SnapEnemy.tick(self)
        self.fridx += 1
        self.texture = EglanBlob.textures[ int(self.fridx/20) % 7 ]

        if(self.firing):
            self.fire_idx += 1
            if self.fire_idx % 12 == 0:
                rad = self.fire_base_rad
                rad += 0.3
                if(self.fire_idx>20):
                    self.fireRanged(rad)
                else:
                    self.flash_color = [ 0.0,0.0,0.0,1.0 ]
            if self.fire_idx > 90:
                self.firing = False
        else:
            self.fire_idx = 0
            self.fire_base_rad = uniform(-3.14,3.14)

        if self.texture == EglanBlob.textures[3]: 

            if(uniform(0.0,1.0)<0.01) and self.mdist(self.floor.player)<40:
                self.firing = True
            if choice([True,False,False]):
                self.v[0] = uniform(-8.0,8.0)
                self.v[1] = uniform(-8.0,8.0)
                if(self.v[1] >0 ):
                    self.size[0] = -7.0
                else:
                    self.size[0] = 7.0

        if self.texture == EglanBlob.textures[4]: 
            if choice([True,False,False]):
                dx = (self.floor.player.p[0] - self.p[0])
                dy = (self.floor.player.p[1] - self.p[1])
                self.v[0] = dx*0.25
                self.v[1] = dy*0.25

        self.light_color = [ abs(sin(self.fridx*0.03)),0.0,abs(cos(self.fridx*0.02)),1.0]

        if(self.hp < 0):
            SnapEnemy.die(self) #@bug physics not cleaned up
            return False
        return True

    def get_shader_params(self):
        sp = Object.get_shader_params(self)
        sp["translation_local"][1] += sin( self.fridx*0.03)*0.08
        return sp

    
    
        


class Elder(Object):
    texture = BGL.assets.get('KT-player/texture/elder0000')
    #texture = BGL.assets.get('KT-forest/texture/cave_entrance')

    def parse(od,df):
        o = Elder( p = [ od["x"], od["y"] ] )
        return o 

    def customize(self):
        self.texture = Elder.texture
        #self.buftarget = "popup"
        self.buftarget = "popup"
        self.size =  [ 6.0, 6.0 ]
        self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
        self.light_color =  [ 1.0,0.4,0.4,1.0]
        self._t = 0.0 
        self.physics = { "radius" : 2.0, "mass"   : 100.0, "friction" : 0.0 } 
        self.tick_type = Object.TickTypes.TICK_FOREVER
        self.z_index = 1

    def tick(self):
        self._t += 0.01
        self.light_radius = (sin(self._t)*85)+110
        dx = self.p[0] - self.floor.player.p[0]
        dy = self.p[1] - self.floor.player.p[1]

        dst = (dx*dx+dy*dy)

        #if(dst<30):
        #    SpeechBubble.instance.set_script(["Oh, it's you.", "Did you know that I talk?", "Yup... I talk.", "I write my text on the floor here, see?", "It's been... a while...","since I met youuuuuu","Ok bye."],  self.p)
        ###    self.floor.player.set_hud_message("HELLO I TALK")
        ###    if self.floor.player.get_pad().button_down( BGL.gamepads.buttons.X ):
        ###        pass


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

        
        

class Shrub(Object):
        textures = [
            BGL.assets.get('KT-forest/texture/shrub0000'),
            BGL.assets.get('KT-forest/texture/shrub0001'),
            BGL.assets.get('KT-forest/texture/shrub0002'),
            BGL.assets.get('KT-forest/texture/shrub0003'),
        ]
        def __init__(self,**kwargs):
            overrides = {
                "physics" : {
                    "radius" : 0.7,
                    "mass"   : 90000.0,
                    "friction" : 0.1
                },
                "buftarget" : "popup"
            }
            overrides.update(kwargs)
            Object.__init__(self,**overrides)
            self.texture = choice( Shrub.textures )
            self.z_index = 1
            sz = uniform(15.0,25.0)
            self.size = [ sz,sz ]
            self.tick_type = Object.TickTypes.TICK_FOREVER
            self.parallax = 1.0
            self.is_shrub = True

        def should_draw(self):
            p = self.get_shader_params()['translation_world']
            visRad = vconf.visRad
            if(p[0]<-visRad): return False
            if(p[1]<-visRad): return False
            if(p[0]>visRad): return False
            if(p[1]>visRad): return False
            return True


        #def get_shader_params(self):
        #    return WarpedPositionObject.warp_shader_params(Object.get_shader_params(self), 0.8,1.2,0.8,1.2)

        ##def get_shader_params(self):
        ##    params = Object.get_shader_params(self)
        ##    tl = params["translation_local"]
        ##    tl[1] = tl[1]
        ##    params["translation_local"] = tl

        ##    tw = params["translation_world"]
        ##    tw[0] = tw[0]*self.parallax
        ##    tw[1] = tw[1]*self.parallax


        ##    z = tw[1]

        ##    minZ = -40.0
        ##    maxZ = 49.0

        ##    z = z + -minZ 
        ##    if(z>maxZ): z = maxZ
        ##    if(z<0.0): z = 0.0

        ##    z = (z / maxZ) + 0.5
        ##   
        ##    s = params["scale_world"]
        ##    s[0] *= z
        ##    s[1] *= z 
        ##    print(z)
        ##    params["translation_world" ] = tw
        ##    return params

class Fire(Object):
        def __init__(self,**kwargs):
            overrides = {
                    'texture' : None,
                    'tick_type' : Object.TickTypes.TICK_FOREVER,
                    'light_radius' : 30.0,
                    'light_type' : Object.LightTypes.DYNAMIC_SHADOWCASTER,
                    'buftarget' : None
                }
            overrides.update(kwargs)
            Object.__init__(self,**overrides)
            self.base_p = self.p
            self.base_radius = self.light_radius

        def tick(self):
            rad_jitter = uniform(0.8,1.2)
            self.light_radius = (self.light_radius*0.9)+(self.base_radius * rad_jitter*0.1)
            jitter = [uniform(-1.2,1.2), uniform(-1.2,1.2) ]
            np = [ self.base_p[0] + jitter[0], self.base_p[1]+jitter[1] ]
            self.p = [ np[0]*0.02 + self.p[0]*0.98,np[1]*0.02 + self.p[1]*0.98 ]
            ncolor = [ uniform(0.6,0.9), uniform(0.3,0.6), uniform(0.1,0.3),1.0]
            for i in range(0,4):
                self.color[i] = self.color[i]*0.9+ncolor[i]*0.1

            return True

        def render(self):
            return



class TreeTop(Object):
        def __init__(self,**kwargs):

            tex_options =  GeneratorOptions.TreeTopTextures

            overrides = {
                    "num" : 0,
                    "texture" : choice(tex_options),
                    'tick_type' : Object.TickTypes.TICK_FOREVER,
                    'size' : [ 5.0,5.0],
                    'rad' : uniform(-3.14,3.14),
                    'parallax' : 1.2,
                    'z_index' : 100,
                    'wind_speed' : uniform(0.1,0.3),
                    'wind_mod' : uniform(1.1,1.2),
                    'buftarget' : 'canopy'
                }


            overrides.update(kwargs)
            Object.__init__(self,**overrides)
            self.t = 0
            self.base_size = [ self.size[0], self.size[1] ]
            self.draw_color = [0.9,uniform(0.8,1.0),0.9,uniform(0.6,0.9)]
            self.last_a = self.draw_color[3]
            #if(self.texture == BGL.assets.get("KT-forest/texture/treetop2")):
            #    self.z_index = self.z_index + 1

        def tick(self):
            self.t = self.t + 0.01
            if(self.should_draw()):
                self.size[0] = self.base_size[0] * ( 4.0 + (1.5*(sin(self.t* self.wind_speed))))
                self.size[1] = self.base_size[1] * ( 4.0 + (1.5*(cos(self.t* self.wind_speed*self.wind_mod))))

            
            return True

        def should_draw(self):
            return True
            #p = self.get_shader_params()['translation_world']
            #visRad = vconf.visRad
            #if(p[0]<-visRad): return False
            #if(p[1]<-visRad): return False
            #if(p[0]>visRad): return False
            #if(p[1]>visRad): return False
            #return True

        def get_shader_params(self):
            params = Object.get_shader_params(self)
            tw = params["translation_world"]
            tw[0] = tw[0]*self.parallax
            tw[1] = tw[1]*self.parallax
            params["translation_world" ] = tw
            params["filter_color"] = list(self.draw_color)

            dx = self.p[0] - (self.floor.camera.p[0]+(self.floor.player.v[0]*3))
            dy = self.p[1] - (self.floor.camera.p[1]+(self.floor.player.v[1]*3))
            md = (dx*dx)+(dy*dy)
            impulse_a = self.draw_color[3]
            if(md < 250):
                impulse_a = 0.1

            self.last_a = (self.last_a * 0.98) + (impulse_a*0.02)
            params["filter_color"][3] = self.last_a
                
            return params

class TreeRoots(Object):
        def __init__(self,**kwargs):
            overrides = {
                    "num" : 0,
                    "texture" : BGL.assets.get("KT-forest/texture/treeroots"),
                    'tick_type' : Object.TickTypes.TICK_FOREVER,
                    'size' : [ 5.0,5.0],
                    'rad' : uniform(-3.14,3.14),
                    'z_index' : -121,
                    'buftarget' : 'floor'
                }
            overrides.update(kwargs)
            Object.__init__(self,**overrides)
            self.t = 0
            self.base_size = [ self.size[0], self.size[1] ]
            self.draw_color = [0.8,uniform(0.0,1.0),0.8,uniform(0.6,0.7)]

        def should_draw(self):
            p = self.get_shader_params()['translation_world']
            visRad = vconf.visRad
            if(p[0]<-visRad): return False
            if(p[1]<-visRad): return False
            if(p[0]>visRad): return False
            if(p[1]>visRad): return False
            return True

        def get_shader_params(self):
            params = Object.get_shader_params(self)
            tw = params["translation_world"]
            params["translation_world" ] = tw
            params["filter_color"] = self.draw_color
            return params

class Rock(Object):
        textures = [
            BGL.assets.get('KT-forest/texture/rock0000'),
            BGL.assets.get('KT-forest/texture/rock0001'),
            BGL.assets.get('KT-forest/texture/rock0002'),
            BGL.assets.get('KT-forest/texture/rock0003'),
        ]
        def __init__(self,**kwargs):
            overrides = {
                    "num" : 0,
                    "texture" : choice( Rock.textures ),
                    'size' : [ 5.0,5.0],
                    'rad' : uniform(-3.14,3.14),
                    'z_index' : -90,
                    'buftarget' : 'popup',
                    'tick_type' : Object.TickTypes.TICK_FOREVER,
                    "physics" : {
                        "radius" : 2.0,
                        "mass"   : 0.02,
                        "friction" : 9000.0
                    },
                }
            overrides.update(kwargs)
            Object.__init__(self,**overrides)
            self.physics["radius"] = self.size[0]*0.5
            self.physics["mass"] = self.physics["mass"] * self.size[0]

        def tick(self):
            self.v[0] = self.v[0]*0.985
            self.v[1] = self.v[1]*0.985
            if(self.should_draw()):
                self.rad = self.rad*0.9+(atan2( self.v[0], self.v[1] )*0.1)

        def should_draw(self):
            p = self.get_shader_params()['translation_world']
            visRad = vconf.visRad
            if(p[0]<-visRad): return False
            if(p[1]<-visRad): return False
            if(p[0]>visRad): return False
            if(p[1]>visRad): return False
            return True

class TreeShadow(Object):
        def __init__(self,**kwargs):
            self.scale = 2
            tt = kwargs['TreeTop']
            overrides = {
                    "num" : 0,
                    "texture" : choice( GeneratorOptions.TreeShadowTextures ),
                    'tick_type' : Object.TickTypes.TICK_FOREVER,
                    'size' : [ self.scale*tt.size[0],self.scale*tt.size[1]],
                    'rad' : tt.rad,
                    'z_index' : 0,
                    'tt' : tt,
                    'buftarget' : 'shadow'
                }
            overrides.update(kwargs)
            Object.__init__(self,**overrides)
            self.t = 0
            self.base_size = [ self.size[0], self.size[1] ]
            self.draw_color = [0.8,uniform(0.0,1.0),0.8,0.3]
            self.wind_speed = tt.wind_speed
            self.wind_mod = tt.wind_mod

        def tick(self):
            TreeTop.tick(self)

        def should_draw(self):
            p = self.get_shader_params()['translation_world']
            visRad = vconf.visRad
            if(p[0]<-visRad): return False
            if(p[1]<-visRad): return False
            if(p[0]>visRad): return False
            if(p[1]>visRad): return False
            return True

        def get_shader_params(self):
            params = Object.get_shader_params(self)
            tw = params["translation_world"]
            params["translation_world" ] = tw
            params["filter_color"] = self.draw_color
            return params

def map_txt_spec( df, txt_spec_raw, probability, times, jitter, effect  ):

    txt_spec = random.sample(txt_spec_raw, len(txt_spec_raw))
    for row_idx,row in enumerate(txt_spec):
        row_spec = row[0]
        for col_idx,char in enumerate(row_spec):
            x = (float(col_idx) / float(len(row_spec))) * float( df.width )
            y = (float(row_idx) / float(len(txt_spec))) * float( df.height )
            if char is not ' ':
                for i in range(0,times):
                    if(uniform(0.0,1.0) < probability ):
                        effect( char,[x+uniform(-1*jitter,jitter),y+uniform(-1*jitter,jitter)] )

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
            #self.generate_trees( dungeon_floor )
            #self.generate_photon_emitters(dungeon_floor)
    
            #self.light_occluders = self.tree_occluders
            self.light_occluders = []
    
    
            #level_data = get_level_data(BGL.assets.get("KT-forest/textfile/totems"), dungeon_floor.width, dungeon_floor.height )
    
    
            #self.map_edges = self.gen_edges( dungeon_floor )
    
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
            #self.generate_static_lights(dungeon_floor)
            #self.generate_fires(dungeon_floor)
            self.generate_tiledata(  dungeon_floor )
    
    
            #self.objects.append( Shrub( p = [0.0,0.0] ) )
            #self.objects.append( TreeRoots( p = [0.0,0.0], size=[5.0,5.0] ) )
            
    #        for x in range(0,40):
    #                px = uniform( -dungeon_floor.width*0.4, dungeon_floor.width*0.4)
    #                py = uniform( -dungeon_floor.height*0.4, dungeon_floor.height*0.4)
    #                self.objects.append( Shrub( p = [px,py] ) )
    #
                    #trs = uniform(15,20)
                    #self.objects.append( TreeRoots( p = [px,py], size=[trs,trs] ) )
    
            ### for x in range(0,250):
            ###         px = uniform( -dungeon_floor.width*0.6, dungeon_floor.width*0.6)
            ###         py = uniform( -dungeon_floor.height*0.6, dungeon_floor.height*0.6)
            ###         rs = uniform(0.8,4.0)
            ###         self.objects.append( Rock( p = [px,py], size = [rs,rs] ) )



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

    def gen_edges(self, df):
        return self.gen_rand_circle_lines( 0.01,0.2, min(df.width,df.height)*0.5)
        ## r = 0.0
        ## points = []
        ## dfilt = None
        ## while(r < 2*pi):
        ##     r = r + uniform(0.01,0.2)
        ##     rad = min(df.width,df.height)*0.5
        ##     d = uniform(0.5*rad, 1.0*rad)
        ##     if dfilt is None:
        ##         dfilt = d
        ##     else:
        ##         dfilt = (d*0.2)+(dfilt*0.8)
        ##     points.append( [ cos(r)*dfilt, sin(r)*dfilt ] )


        ### lines = []
        ### for i in range(0, len(points)-1):
        ###     lines.append( [ points[i],points[i+1]] )

        ### lines.append( [ points[len(points)-1],points[0]] )
        ## lines = [
        ##     [ [-0.5*df.width, -0.5*df.height],[0.5*df.width, -0.5*df.height] ],
        ##     [ [ 0.5*df.width, -0.5*df.height],[0.5*df.width, 0.5*df.height] ],
        ##     [ [0.5*df.width, 0.5*df.height],[-0.5*df.width, 0.5*df.height] ],
        ##     [ [-0.5*df.width, 0.5*df.height],[-0.5*df.width, -0.5*df.height] ]
        ## ]
        return lines

    def get_light_occluders(self):

        return self.light_occluders

    def get_tiledata(self):
        return self.tile_data

    def get_photon_emitters(self):
        return self.photon_emitters

    def get_sigil_tiledata( self, sigil ):

        if sigil == "#":
            return choice( range(1,20) )
        if sigil == "_":
            return choice( range(10,20) )
        if sigil == "y":
            return choice( range(5,15) )
        if sigil == "`":
            return choice( range(1,10) )
        if sigil == "X":
            return choice( range(2,18) )
        exit()


    
    def evaluate_tile(self,rx,ry):

        #d  = hypot(rx - self.df.player.p[0], ry-self.df.player.p[1])

        #if( d<10):
        #    return 1
        #else:
        #    return 15

        self.vpts.sort( key = lambda x: hypot(rx-x[1],ry-x[2]) )
        #win_d = 0
        #win_range = None 
        #second_range = None
        #for pt in self.vpts:
        #    d = hypot(rx-pt[1], ry-pt[2])
        #    if win_range is None:
        #        win_d = d
        #        win_range = pt[0]
        #        second_range = win_range
        #    else:
        #        if( d< win_d):
        #            win_d = d
        #            second_range = win_range
        #            win_range = pt[0]

        #

        win_range = self.vpts[0][0]
        return choice( win_range )
                 

    
    def generate_voroni_pts(self):
        self.vpts = []

        self.width = self.df.width #i give up
        self.height = self.df.height

        for pt in self.tree_pts:
            self.vpts.append( ( (1,19) , pt[0], pt[1] ) )

        for pt in self.guider_pts:
            self.vpts.append( ( (1,10) , pt[0], pt[1] ) )


        #for pobj in filter( lambda x: "portal_target" in x.__dict__, self.objects):
        #    self.vpts.append( ( (5,15) , pobj.p[0], pobj.p[1] ) )

        #for pobj in filter( lambda x: "is_shrub" in x.__dict__, self.objects):
        #    self.vpts.append( ( (15,19) , pobj.p[0], pobj.p[1] ) )


    def generate_tiledata( self, df ):

        self.df = df #i give up
        #self.generate_voroni_pts()

        print('')
        print(df.tilemap_width)
        print(df.tilemap_height)
        tile_data = [0]*(df.tilemap_width*df.tilemap_height)
        for tile_def in self.ad["tile_defs"]:
            addr = tile_def["x"] + (tile_def["y"]*df.tilemap_width)
            tile_data[addr] = tile_def["idx"] + 1
    
            


        ##### tile_rows = []
        ##### for row in range(0, df.tilemap_height):
        #####     tile_rows.append( [None] * df.tilemap_height )
        ##### for mline in self.magic_lines:
        #####     line = mline['line']
        #####     line['x1'] = int(((line['x1'] / (df.width)) * df.tilemap_width) + (df.tilemap_width/2))
        #####     line['y1'] = int(((line['y1'] / (df.height)) * df.tilemap_height) + (df.tilemap_height/2))
        #####     line['x2'] = int(((line['x2'] / (df.width)) * df.tilemap_width) + (df.tilemap_width/2))
        #####     line['y2'] = int(((line['y2'] / (df.height)) * df.tilemap_height) + (df.tilemap_height/2))

        #####     print(line)
        #####     pts = vscan_line((line['x1'],line['y1']), (line['x2'],line['y2']))
        #####     for pt in pts:
        #####         print(pt[0],pt[1])
        #####         tile_rows[pt[1]][pt[0]] = mline['magic_number']

        ##### 
        ##### for row_num, row in enumerate(tile_rows):

        #####     print("ROW", row)
        #####     converted = fill_scanline( row )
        #####     print("SCANNED", converted)
        #####     for x, cell in enumerate(converted):
        #####         addr = (row_num * df.tilemap_width) + x
        #####         tile_data[addr] = cell
        #####     

        ##### #exit()
        self.tile_data = tile_data;
            
                
        return;

        for x in range(0, df.tilemap_width):
            for y in range(0, df.tilemap_height):
                ####### closest_sigil_point = None
                ####### score = None
                ####### for sigil_point in self.sigil_points:

                #######     a =sigil_point["p"][0]-x
                #######     b =sigil_point["p"][1]-y
                #######     d = abs(a) + abs(b)
                #######     if not score:
                #######         score = d
                #######         closest_sigil_point = sigil_point
                #######     elif d < score:
                #######         closest_sigil_point = sigil_point
                #######         score = d
                ####### tile_data[  (y * df.width) + x ]  = self.get_sigil_tiledata(closest_sigil_point["sigil"])


                
                rx = float(((x*df.tilescale)-((df.tilemap_width*df.tilescale)/2)))
                ry = float(((y*df.tilescale)-((df.tilemap_height*df.tilescale)/2)))

                tval = self.evaluate_tile(rx,ry)
                #tval = 1

                tile_data[  (y * df.tilemap_width) + x ]  = tval

        self.tile_data = tile_data

    def generate_static_lights(self, df):
        static_lights = []
        # txt_spec = [
        #     [ "  1     1  " ],
        #     [ " 2   3   2 " ],
        #     [ "  1     1  " ]
        # ]

        txt_spec = choice(light_specs)

        def generate_light(char, p):
            p[0] = p[0]-(df.width/2) + uniform(-1.0,1.0)
            p[1] = p[1]-(df.height/2) + uniform(-1.0,1.0)

            light_styles = {
                '1' : [ Object.LightTypes.STATIC_SHADOWCASTER, [ 0.1,0.3,0.1,1.0], 15.0 ],
                '2' : [ Object.LightTypes.STATIC_SHADOWCASTER, [ 0.5,0.3,0.8,1.0], 25.0 ],
                '3' : [ Object.LightTypes.STATIC_SHADOWCASTER, [ 0.8,0.6,0.0,1.0], 40.0 ],
            }

            style = light_styles[char]

            return [ Object( visible = False, light_type = style[0], p = p, light_radius=style[2], color = list( map( lambda x: x*0.8,style[1]))) ]


        for x in range(0,25):
            p = [ uniform(-0.5,0.5)*df.width, uniform(-0.5,0.5)*df.height ]
            static_lights.extend( generate_light(choice(['1','2','3']),p) )
        #map_txt_spec( df, txt_spec, 1.0, 2, 25.0, lambda char, p : static_lights.extend(generate_light(char, p)))
        self.objects.extend( static_lights )


    def make_guider_photons(self,df):
        photon_emitters = []
        for guider in self.guiders:

            res = 12.
            dx = (guider[1][0]-guider[0][0])/res
            dy = (guider[1][1]-guider[0][1])/res

            for i in range(0,int(res)):
                if(uniform(0.0,1.0) < 0.3):
                    continue
                idx = float(i) / res
                x = guider[0][0] + (dx*float(i))
                y = guider[0][1] + (dy*float(i))

                self.guider_pts.append([x,y])
                color_a = [1.0,1.0,0.0,0.3]
                color_b = [0.0,0.0,1.0,1.0]

                for i in range(0,3):
                    color_a[i] = color_a[i] + uniform(-0.1,0.1)
                    color_b[i] = color_b[i] + uniform(-0.1,0.1)

                idx = idx + uniform(-0.1,0.1)
                color = [ 
                    (idx*color_a[0]) + ((1.0-idx)*color_b[0]),
                    (idx*color_a[1]) + ((1.0-idx)*color_b[1]),
                    (idx*color_a[2]) + ((1.0-idx)*color_b[2]),
                    1.0 ]
                emitter_def = [ x,y, 1.0,1.0, color ]
                photon_emitters.append(emitter_def)
    
            #p = guider[0] 
            #emitter_def = [ p[0],p[1], 15.0,15.0, [1.0,0.0,0.0,1.0] ]
            #photon_emitters.append(emitter_def)
            #p = guider[1] 
            #emitter_def = [ p[0],p[1], 15.0,15.0, [0.0,0.0,1.0,1.0] ]
            #photon_emitters.append(emitter_def)
        
        self.photon_emitters = photon_emitters
    

    def generate_photon_emitters(self, df):
        photon_emitters = []
        txt_spec = choice( photon_specs )
        ##txt_spec = [
        ##    [ "2,,,,,,2" ],
        ##    [ ",2,11,2," ],
        ##    [ ",1,13,1," ],
        ##    [ "3,1113,3" ],
        ##    [ "1,,31,2," ],
        ##    [ ",2,11,2," ],
        ##    [ "2,,1,,,2" ]
        ## ]

        def generate_emitter(char,p):
            if char is ',':
                return []
            p[0] = p[0]-(df.width/2) + uniform(-1.0,1.0)
            p[1] = p[1]-(df.height/2) + uniform(-1.0,1.0)

            colormap = {
                "1" : [ 0.3,0.5,0.4 ], #moonlight?
                "2" : [ 0.3,0.2,0.01 ], #sinister red?
                "3" : [ 0.5,0.61,0.3 ], #desaturated evening light?
            }
            emitter_def = [ p[0],p[1], 1.0,1.0, colormap[char] ]
            return [ emitter_def ]

        map_txt_spec( df, txt_spec, 0.6, 3, 3.0, lambda char, p : photon_emitters.extend(generate_emitter(char, p)))
        self.photon_emitters = photon_emitters

    def generate_trees( self, df ):
        ##txt_spec = [
        ##    [ "Q Q Q Q Q Q Q Q Q Q" ],
        ##    [ "Q _ _`_ _ _ ` _ _ Q" ],
        ##    [ "Q_ ee` yyyy_`_ee _Q" ],
        ##    [ "Q_ ee` yyyy_`_ee _Q" ],
        ##    [ "Q_ _ ` ` ` ``Q _ _Q" ],
        ##    [ "Q_ ee_y_ _y_ _ee _Q" ],
        ##    [ "Q_ ee_ _ ` _ yee _Q" ],
        ##    [ "Q_ _ y _ ` _ ___y_Q" ],
        ##    [ "Q_ ee_ _Q` _ _ee _Q" ],
        ##    [ "Q_ ee_ _ ` _ _ee _Q" ],
        ##    [ "Q_ _ _y_ ` y _ _ _Q" ],
        ##    [ "Q Q Q Q Q Q Q Q Q Q" ] ]
        txt_spec = choice(tree_specs)

        tree_occluders = []

        def generate_tree_objects(char,p):
            size = None
            if char == "Q":
                size = uniform(5,15)
            if char == "e":
                size = uniform(3,7)
            if char == "`":
                size = uniform(2,5)
            if(size is None):
                return []
            p[0] = p[0]-(df.width/2) + uniform(-1.0,1.0)
            p[1] = p[1]-(df.height/2) + uniform(-1.0,1.0)


            self.tree_pts.append(p)
            return [ TreeTop( p = p, size = [ size*0.6, size*0.6 ], parallax = uniform(1.1,1.8) ) ]

        def generate_tree_occluders(char,p):
            size = None
            if char == "Q":
                size = uniform(3.5,16.2)
            if char == "e":
                size = uniform(1.3,5.6)
            if char == "`":
                size = 0.6


            if(size is None or uniform(0.0,1.0) < 0.5):
                return []

            p[0] = p[0]-(df.width/2) + uniform(-1.0,1.0)
            p[1] = p[1]-(df.height/2) + uniform(-1.0,1.0)
            points = []

            points.append( [ 0.0, -1*size ] )
            points.append( [ 0.5*size, -0.5*size ] )
            points.append( [ size, 0.0 ] )
            points.append( [ 0.5*size, 0.5*size ] )
            points.append( [ 0.0, 1*size ] )
            points.append( [ -0.5*size, 0.5*size ] )
            points.append( [ -1*size, 0.0 ] )
            points.append( [ -0.5*size, -0.5*size ] )

            for point in points:
                point[0] = point[0] + p[0] + uniform(-0.1 * size, 0.1*size )
                point[1] = point[1] + p[1] + uniform(-0.1 * size, 0.1*size )

            lines = []
            lines.extend( [ [ points[0], points[1] ] , [ points[1], points[2] ] , [ points[2], points[3] ] , [ points[3], points[0] ] ] )
            return lines

        tree_objects = []
        map_txt_spec( df, txt_spec, 0.9, 4, 5.0, lambda char, p : tree_objects.extend(generate_tree_objects(char, p)))
        tree_objects.sort( key =lambda x: x.parallax )
        self.objects.extend(tree_objects)

        map_txt_spec( df, txt_spec, 1.0, 2, 2.0, lambda char, p : tree_occluders.extend(generate_tree_occluders(char, p)))
        self.tree_occluders = tree_occluders

    def generate_sigil_points( self, df):
        #txt_spec = [
        #    [ "# # # # # # # # # #" ],
        #    [ "# _ _`_ _ _ ` _ _ #" ],
        #    [ "#_ XX` yyyy_`_XX _#" ],
        #    [ "#_ XX` yyyy_`_XX _#" ],
        #    [ "#_ _ ` ` ` ``_ _ _#" ],
        #    [ "#_ XX_ _ _ _ _XX _#" ],
        #    [ "#_ XX_ _ ` _ _XX _#" ],
        #    [ "#_ _ _ _ ` _ ___ _#" ],
        #    [ "#_ XX_ _ ` _ _XX _#" ],
        #    [ "#_ XX_ _ ` _ _XX _#" ],
        #    [ "#_ _ _ _ ` _ _ _ _#" ],
        #    [ "# # # # # # # # # #" ] ]

        txt_spec = choice( sigil_specs )
        sigil_points = []

        map_txt_spec( df, txt_spec, 0.8, 2, 1.0, lambda char, p : sigil_points.append({ "sigil": char, "p": p } ) )
        self.sigil_points = sigil_points


###class WarpedPositionObject():
###
###    def warp_shader_params(params,minx,maxx,miny,maxy):
###
###        screen_x = params["translation_world"][0] * params["scale_world"][0] * params["view"][0]
###        screen_y = params["translation_world"][1] * params["scale_world"][1] * params["view"][1]*-1
###
###        #emulate dist parallax warp
###        from_c = (hypot(screen_x*1.7,screen_y))*1.2
###        parallax_ratio = 0.1 * from_c
###
###        #emulate letterbox
###        screen_x = (screen_x * 0.7) + (0.15)
###        screen_y = (screen_y * 0.7) + (0.15)
###
###        screen_x = screen_x * (1.0+(parallax_ratio*from_c))
###        screen_y = screen_y * (1.0+(parallax_ratio*from_c))
###
###        scale_index = max(min(1.0,(screen_y*0.5)+0.5),0.0)
###
###        print(scale_index)
###
###        offsx = (scale_index * (maxx-minx))+minx 
###        offsy = (scale_index * (maxy-miny))+miny
### 
###
###        screen_x = screen_x*offsx
###        screen_y = screen_y*offsx
###
###
###        params["translation_world"][0] = (screen_x / params["view"][0]) / params["scale_world"][0]
###        params["translation_world"][1] = ((screen_y*-1) / params["view"][1]) / params["scale_world"][1]
###        #print(scale_index)
###        #print(screen_x,screen_y)
###        return params
###
