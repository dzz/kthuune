#### MACHINE GIRL 
#### BATMAN 
#### ZELDA
#### STIMULANTS
#### PAGANISM
#### BREAKCORE TEMPOS
#### SIEZURES
#### DARK SOULS
#### X FILES

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

from ..KSounds import KSounds

from ..GeneratorOptions import GeneratorOptions

class Blood(Object):
    texture = [
        BGL.assets.get("KT-forest/texture/blood0000"),
        BGL.assets.get("KT-forest/texture/blood0001"),
        BGL.assets.get("KT-forest/texture/blood0002"),
        BGL.assets.get("KT-forest/texture/blood0003"),
    ]

    def customize(self):
        self.rad = uniform(0.0,3.14*2)
        self.size = [ 3.0+uniform(0.0,1.0),3.0+uniform(0.0,1.0)]
        self.buftarget = "floor"
        self.tick_type = Object.TickTypes.STATIC
        self.texture = choice(Blood.texture)
        pass

class HealthVial(Object):
    textures = [ 
        BGL.assets.get("KT-player/texture/healthvial0000"),
        BGL.assets.get("KT-player/texture/healthvial0001"),
    ]
   
    def customize(self):
        self.fridx = 0
        self.texture = HealthVial.textures[0]
        self.buftarget = "popup"
        self.base_p = list(self.p)
        self.tick_type = Object.TickTypes.PURGING
        self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
        self.light_color = [ 1.0, 0.0, 0.0, 1.0 ]
        self.light_radius = 10.
        self.trigger_timer = 0
        self.visible = False

    def tick(self):
        self.trigger_timer = self.trigger_timer + 1
       
        if self.trigger_timer<30:
            return True 

        self.visible = True

        self.fridx = (self.fridx + 1) % 40
        self.texture = HealthVial.textures[int(self.fridx/20)]
 
        y_offs = sin(self.fridx*(6.28/40.0))

        self.rad = y_offs*0.1

        self.p[1] = self.base_p[1] + (y_offs*0.15)

        dx = self.p[0] - self.floor.player.p[0]
        dy = self.p[1] - self.floor.player.p[1]

        md = (dx*dx) + (dy*dy)

        if (md<2):
            if(self.floor.player.has_inv()):
                self.floor.objects.remove(self)
                self.floor.player.add_inv("hp_vial")
                KSounds.play( KSounds.pickup )
                return False

        return True

class AttackInfo(Object):
    def customize(self):
        self.tick_type = Object.TickTypes.PURGING
        self.buffer = BGL.framebuffer.from_dims( len(self.message)*8, 8)
        self.texture = self.buffer.get_texture()      
        self.buftarget = "hud"
        self.size = [ 1.0*len(self.message), -1.0 ]

        self.lifetime = 100
        with BGL.context.render_target(self.buffer):
            BGL.context.clear(0.0,0.0,0.0,0.0)
            BGL.lotext.render_text_pixels( self.message, 0,0, [1.0,1.0,1.0] )

    def tick(self):
        if self.lifetime<60:
            self.size[0] *= 1.28
            self.size[1] *= 1.28
    
        if self.lifetime<80:
            self.color[3] = self.color[3]*0.95
            self.color[0] = uniform(0.0,1.0)
            self.color[1] = uniform(0.0,1.0)
            self.color[2] = uniform(0.0,1.0)

        if self.lifetime>0:
            self.lifetime -=1
            return True
        else:
            self.floor.objects.remove(self)
            return False


class FactoryLight(Object):
    def customize(self):
        self.visible = False
        self.tick_type = Object.TickTypes.STATIC
        self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
        self.light_radius = 100
        self.p = [ self.factory_def['x'], self.factory_def['y'] ]
        if self.factory_def["meta"]["class"] == "red_test":
            self.light_color = [ 1.0, 0.2,0.2,1.0 ]
        if self.factory_def["meta"]["class"] == "blue_test":
            self.light_color = [ 0.2, 0.2,1.0,1.0 ]
        if self.factory_def["meta"]["class"] == "green":
            self.light_radius = 25.
            self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
            self.light_color = [ 0.5, 1.0,0.8,1.0 ]

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
        self.open_speed = 0.1
        self.close_speed = 0.2
    
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
        

class SnapEnemy(Object):
    TOTEM = 0
    ENEMY = 1


    def custom_die(self):
        pass
    def can_see_player(self):
        test_segment = [ [ self.floor.player.p[0], self.floor.player.p[1] ], [self.p[0], self.p[1] ] ]
        for segment in self.floor.get_light_occluders():
            if segments_intersect( segment, test_segment ):
                return False
        return True

    def die(self):
        if self in self.floor.objects:
            #hack
            self.floor.objects.remove(self)
        if(self in self.floor.snap_enemies):
            self.floor.snap_enemies.remove(self)
        self.floor.create_object( SkullDeath( p = [ self.p[0], self.p[1] ] ) )
        self.floor.player.set_hud_message("KILL!", 60)
        self.floor.player.notify_enemy_killed()
        self.floor.freeze_frames = 3
        
        if(uniform(0.0,1.0) > 0.85):
            self.floor.create_object(HealthVial(p=[ self.p[0], self.p[1]]))

        self.floor.create_object(Blood(p=[self.p[0],self.p[1]]))
        self.custom_die()
        for x in range(0,self.get_kill_particles()):
            spltr = SplatterParticle( p = [self.floor.player.p[0], self.floor.player.p[1]], rad = uniform(-3.14,3.14))
            spltr.color = [0.0,0.0,0.0,1.0]
            spltr.light_color = [ 0.0,1.0,0.0,1.0]
            spltr.size[0]*=uniform(1.0,1.5)
            self.floor.create_object(spltr)


    def get_kill_particles(self):
        return 25

    def parse(od,df):
        o = SnapEnemy( p = [ od["x"],od["y"] ] )
        df.snap_enemies.append(o)
        return o

    def raise_critical_attack(self):
        self.snap_effect_emit = 20
        self.floor.player.notify_crit()
        self.floor.create_object( SwordCrit( p = [ self.p[0], self.p[1]-30 ]))

    def receive_snap_attack(self, was_crit):
        self.iframes = 20
        self.snap_effect_emit = 10

        crit = 1

        #if(uniform(0.0,1.0)< (self.floor.player.crit_chance*self.floor.player.get_crit_mod())):
        if was_crit:
            crit = 1.8
            print("CRITICAL")
            self.raise_critical_attack()

        attack_amt = (self.floor.player.attack_str*crit) - self.defense

        if(attack_amt<=0):
            attack_amt = 1

        attack_amt += uniform(0, self.floor.player.attack_bonus) * self.floor.player.attack_str

        attack_amt = floor(attack_amt)
        print("ATTACK -> {0}".format(attack_amt))

        self.floor.create_object(AttackInfo( p=[ self.p[0], self.p[1] ], message="{0}".format(attack_amt)))
        self.hp = self.hp - attack_amt

        for x in range(0,11):
            spltr = SplatterParticle( p = [self.floor.player.p[0], self.floor.player.p[1]], rad = uniform(-3.14,3.14))
            spltr.color = [0.0,0.0,0.0,1.0]
            spltr.light_color = [ 0.0,1.0,0.0,1.0]
            spltr.size[0]*=uniform(1.0,1.5)
            self.floor.create_object(spltr)

        if self.floor.player.snap_animation_buffer>0 and self.hp<=0:
            r = self.tick()
            if not r:
                self.floor.purging_tick_manager.tickables.remove(self)

    def tick(self):

        if(self.iframes>0):
            self.iframes -=1
        if(self.snap_effect_emit>0):
            self.snap_effect_emit = self.snap_effect_emit - 1
            self.floor.create_object( Splat( p = self.p ) )

        self.light_radius = uniform(2.0,12.0)
        return True

    def customize(self):
        self.snap_type = SnapEnemy.ENEMY
        self.snap_effect_emit = 0
        self.tick_type = Object.TickTypes.PURGING
        self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
        self.light_radius = 10.0
        self.light_color = [ 1.0, 0.8, 0.0, 1.0 ]
        self.visible = True
        self.z_index = 1
        self.buftarget = "popup"
        self.texture = Skeline.textures[2]
        self.size = [ 1.75, 1.75 ]
        self.set_combat_vars(self)

    def set_combat_vars(self):
        self.hp = 85
        self.defense = 10

class AreaSwitch(Object):
    def customize(self):
        self.visible = False
        self.tick_type = Object.TickTypes.TICK_FOREVER
        self.trigger_active = True
        self.rad2 = 15
        self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
        self.light_color =  [ 2.8,2.7,2.0,1.0]
        self.light_radius = 5.0

    def tick(self):
        dx = self.floor.player.p[0] - self.p[0]
        dy = self.floor.player.p[1] - self.p[1]
        d2 = (dx*dx)+(dy*dy)

        if not self.trigger_active:
            self.light_radius = 0.1
        else:
            if self.light_radius < 5.0:
                self.light_radius = self.light_radius*1.2
        if d2 > (self.rad2*5):

            self.trigger_active = True
        if self.trigger_active:
            if d2 < (self.rad2*10):
                self.floor.player.set_hud_message("go to {0} - {1}".format(self.target_area, self.target_switch))
            if d2 < self.rad2:
                self.trigger()

    def trigger(self):
        self.floor.game.next_area( self.target_area, self.target_switch )

class Prop(Object):
    def parse(pd):
        p = Prop( texture = BGL.assets.get("KT-props/texture/" + pd["image"]))
        p.p[0] = pd["x"]
        p.p[1] = pd["y"]
        p.size[0] = pd["w"]
        p.size[1] = pd["h"]
        p.r = pd["r"]

        p.z_index = 1
        p.buftarget="popup"
        return p


class Sword(Object):
    STATE_IDLE = 0
    STATE_CHARGING = 1
    STATE_ATTACK_PENDING = 2
    STATE_DISCHARGING = 3
    STATE_AWAITING_RELEASE = 4
    STATE_SPIN_ATTACK = 5

class vconf():
    visRad = 50

class SplatterParticle(Object):
    def __init__(self,**kwargs):
        Object.__init__(self,**kwargs)
        self.texture = choice(Blood.texture)
        self.buftarget = "popup"
        self.tick_type = Object.TickTypes.PURGING
        self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
        self.light_radius = 15
        self.lifespan = 90
        self.light_color = [ 1.0,0.7,0.0,0.0 ]
        self.color = [1.0,0.5,0.5,1.0]

        self.size = [ 2.8,2.8 ]
        self.snapshot_fields = [ 'p' ]

        spd = 0.3 + uniform(0.2,0.8)
        self.vx = cos( self.rad )*spd
        self.vy = sin( self.rad )*spd
        self.rad = uniform(-3.14,3.14)

        
    def tick(self):
        self.color[3]*=uniform(0.98,0.999)
        self.light_radius*=0.95
        self.vx*=0.9
        self.vy*=0.9
        self.vy+=0.02
        self.p[0] = self.p[0] + self.vx 
        self.p[1] = self.p[1] + self.vy 

        self.size[0]*=0.94
        self.size[1]*=0.94
        self.lifespan = self.lifespan-1
        if(self.lifespan<0):
            self.floor.objects.remove(self)
            return False
        return True

class ERangedMagic(Object):
    arrow_texture = BGL.assets.get("KT-player/texture/flare")
    def __init__(self,**kwargs):
        Object.__init__(self,**kwargs)
        self.texture = ERangedMagic.arrow_texture
        self.buftarget = "popup"
        self.tick_type = Object.TickTypes.PURGING
        self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
        self.light_radius = 5
        self.lifespan = 120
        self.light_color = [ 0.6,1.0,0.3,0.4 ]

        self.size = [ 0.5,0.5 ]
        self.snapshot_fields = [ 'p' ]

        spd = 0.55 + uniform(0.001, 0.01)
        self.vx = cos( self.rad )*spd
        self.vy = sin( self.rad )*spd
        
        self.attack_str = 8
        
    def tick(self):

        deadly = False
        if(self.size[0] < 1.5):
            growth = 1.2
            self.size[0] *= growth
            self.size[1] *= growth
        else:
            deadly = True
        self.light_color[1] = uniform(0.4,0.8)
        self.light_color[0] = uniform(0.0,1.0)
        self.light_color[3] = uniform(0.0,1.0)
        self.light_radius = uniform(15,40)
        self.p[0] = self.p[0] + self.vx 
        self.p[1] = self.p[1] + self.vy 
        self.lifespan = self.lifespan - 1

        segment = [
                    [self.snapshot['p'][0], self.snapshot['p'][1]],
                    [self.p[0], self.p[1] ]
                  ]

        for blocker in self.floor.get_light_occluders():
            if segments_intersect( segment, blocker):
                self.lifespan = 0
                break                

        if not deadly:
            return True

        dx = self.p[0] - self.floor.player.p[0]
        dy = self.p[1] - self.floor.player.p[1]
    
        dx = dx * dx
        dy = dy * dy

        md = dx+dy

        if md < 3:
            self.floor.player.receive_ranged_attack(self)
            self.floor.create_object( Splat( p = self.p, color=[1.0,0.0,0.0,1.0] ) )
            self.floor.objects.remove(self)

            for x in range(0,25):
                self.floor.create_object(SplatterParticle( p = [self.floor.player.p[0], self.floor.player.p[1]], rad = uniform(-3.14,3.14)))
            
            return False

        if(self.lifespan>0):
            return True
        self.floor.objects.remove(self)
        return False

class Acolyte(SnapEnemy):
    def custom_die(self):
        wf_spec = [ self.p[0], self.p[1], 15 ]
        self.floor.create_object( WormField( wf_spec = wf_spec) )
        for enemy in self.floor.snap_enemies:
            if enemy.snap_type == SnapEnemy.ENEMY:
                if enemy.triggered:
                    enemy.receive_snap_attack(True)

    def receive_snap_attack(self, was_crit):
        SnapEnemy.receive_snap_attack(self, was_crit)
        self.stimer = 0
        self.state = Acolyte.STATE_CHARGING_SHOT

    def parse(od,df):
        o = Acolyte( p = [ od["x"],od["y"] ] )
        df.snap_enemies.append(o)
        return o

    STATE_SEEKING_RANDOM = 0
    STATE_SEEKING_PLAYER = 1
    STATE_CHARGING_SHOT = 2
    STATE_FIRING_SHOT = 3

    textures = [
        BGL.assets.get("KT-forest/texture/acolyte0000"),
        BGL.assets.get("KT-forest/texture/acolyte0001"),
        BGL.assets.get("KT-forest/texture/acolyte0002")
    ] 
    def customize(self):
        self.is_acolyte = True
        self.fire_count = 0
        self.triggered = False
        self.tick_type = Object.TickTypes.PURGING
        self.snap_type = SnapEnemy.ENEMY
        self.visible = True
        self.z_index = 1
        self.buftarget = "popup"
        self.texture = Acolyte.textures[0]
        self.widx = int(uniform(0.0,40.0))
        self.size = [ 4, 4 ]
        self.physics = { "radius" : 0.35, "mass"   : 0.0005, "friction" : 0.3 }
        #self.state = choice( [ Acolyte.STATE_SEEKING_RANDOM, Skeline.STATE_SEEKING_PLAYER ] )
        self.state = Acolyte.STATE_SEEKING_RANDOM
        self.stimer = 0
        self.rvx = None
        self.speed = 0.8
        self.invert_seek = False
        self.flip_pxy = False

        self.wavidx = 0
        self.snap_effect_emit = 0
        self.iframes = 0
        SnapEnemy.set_combat_vars(self)

        self.hp = 250
        

    def tick(self):

        if self.triggered:
            self.floor.add_fog(self, 0.7)
        self.wavidx = self.wavidx + 0.01
        SnapEnemy.tick(self)
        self.widx = (self.widx + 1) % 40
        self.wfr = floor(self.widx/20)
        self.texture = Acolyte.textures[0]
        self.light_type = Object.LightTypes.NONE

        y = self.floor.player.p[0] - self.p[0]
        x = self.floor.player.p[1] - self.p[1]

        md = (x*x)+(y*y)
        if( md < 250 ):
            if not self.triggered:
                self.triggered = True
                if not self.can_see_player():
                    self.triggered = False

        if( md > 300 ):
            self.triggered = False

        if not self.triggered:
            if(self.hp < 0):
                SnapEnemy.die(self)
                return False
            #self.visible = False
            return True

        self.visible = True

        self.stimer = self.stimer + 1

        calc_speed = self.speed

        if self.state == Acolyte.STATE_SEEKING_PLAYER:
            if(self.stimer == 1):
                KSounds.play(KSounds.acolyte_hustle)
            self.fire_count = 0
            self.rvx = None
            if self.flip_pxy:
                y = self.floor.player.p[0] - self.p[0]
                x = self.floor.player.p[1] - self.p[1]
            else:
                x = self.floor.player.p[0] - self.p[0]
                y = self.floor.player.p[1] - self.p[1]
    


            rad = atan2(y,x)
            vx = cos(rad) * calc_speed
            vy = sin(rad) * calc_speed
            self.v = [ vx,vy]

            if(self.stimer > 25 ):
                self.stimer = 0
                self.state = choice( [ Acolyte.STATE_SEEKING_RANDOM, Skeline.STATE_SEEKING_PLAYER ] )
                self.invert_seek = choice( [ True, False ] )
                if( self.state == Acolyte.STATE_SEEKING_RANDOM ):
                    self.state = choice( [ Acolyte.STATE_SEEKING_RANDOM, Skeline.STATE_CHARGING_SHOT ] )
                    self.flip_pxy = choice( [ True, True, True, False ] )
        if self.state == Acolyte.STATE_SEEKING_RANDOM:
            self.fire_count = 0
            if not self.rvx:
                self.rvx = [ uniform(-1.0,1.0), uniform(-1.0,1.0) ]
                self.flip_pxy = choice( [ True, False ] )
            self.v = [ self.rvx[0] * calc_speed, self.rvx[1] * calc_speed ]
            if(self.stimer > 80 ):
                self.stimer = 0
                self.state = choice( [ Acolyte.STATE_SEEKING_RANDOM, Skeline.STATE_SEEKING_PLAYER, Skeline.STATE_CHARGING_SHOT ] )
                self.invert_seek = choice( [ True, True,True, False ] )
        if self.state == Acolyte.STATE_CHARGING_SHOT:
            if(self.stimer == 10):
                KSounds.play(KSounds.acolyte_hustle)
            self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
            self.light_color = [9.0,0.4,0.1,1.0]
            self.light_radius = uniform(30.0,50.0)
            self.v = [0.0,0.0]
            self.texture = Acolyte.textures[1]
            self.floor.create_object( Flare( p = [ self.p[0], self.p[1] ] ) )
            if( self.stimer > 25 ):
                self.stimer = 0
                self.state = Acolyte.STATE_FIRING_SHOT
                self.pickTarget()
        if self.state == Acolyte.STATE_FIRING_SHOT:
            if(self.stimer==1):
                KSounds.play_eproj()
            self.texture = Acolyte.textures[2]
            if( self.stimer > 8 ):
                self.fireRanged()
                self.fire_count = self.fire_count + 1
                if self.fire_count >3:
                    self.state = Acolyte.STATE_SEEKING_PLAYER
                    self.fire_count = 0
                else:
                    self.state = Acolyte.STATE_CHARGING_SHOT

        if(self.hp < 0):
            SnapEnemy.die(self)
            return False

        return True

    def pickTarget(self):
        x = self.floor.player.p[0] - self.p[0]
        y = self.floor.player.p[1] - self.p[1]
        rad = atan2(y,x)
        self.target_rad = rad
        
    def fireRanged(self):
        #x = self.floor.player.p[0] - self.p[0]
        #y = self.floor.player.p[1] - self.p[1]
        #rad = atan2(y,x)
        self.floor.create_object( ERangedMagic( p = [ self.p[0], self.p[1] ], rad = self.target_rad+uniform(-0.1,0.1) ) )
        KSounds.play_eproj()

    def get_shader_params(self):
        bp = Object.get_shader_params(self)
        bp['translation_local'][0] = 0.1
        bp['translation_local'][1] = -0.4 + (sin( self.wavidx )*0.2)
        return bp

class Stork(SnapEnemy):

    def custom_die(self):
        wf_spec = [ self.p[0], self.p[1], 15 ]
        self.floor.create_object( WormField( wf_spec = wf_spec) )

    def get_shader_params(self):
        bp = Object.get_shader_params(self)
        bp['translation_local'][0] = 0.1
        bp['translation_local'][1] = -0.4
        return bp

    def receive_snap_attack(self, was_crit):
        SnapEnemy.receive_snap_attack(self, was_crit)

    def parse(od,df):
        o = Stork( p = [ od["x"],od["y"] ] )
        df.snap_enemies.append(o)
        return o

    STATE_WAITING = 0
    STATE_LEAPING = 1
    STATE_LANDING = 2

    textures = [
        BGL.assets.get("KT-forest/texture/stork0000"),
        BGL.assets.get("KT-forest/texture/stork0001"),
        BGL.assets.get("KT-forest/texture/stork0002")
    ] 
    def customize(self):
        self.fire_count = 0
        self.triggered = False
        self.tick_type = Object.TickTypes.PURGING
        self.snap_type = SnapEnemy.ENEMY
        self.visible = True
        self.z_index = 1
        self.buftarget = "popup"
        self.texture = Stork.textures[0]
        self.widx = int(uniform(0.0,40.0))
        self.size = [ 4, 4 ]
        self.physics = { "radius" : 0.35, "mass"   : 0.0005, "friction" : 0.0 }
        #self.state = choice( [ Stork.STATE_SEEKING_RANDOM, Skeline.STATE_SEEKING_PLAYER ] )
        self.state = Stork.STATE_WAITING
        self.stimer = 0
        self.rvx = None
        self.speed = 0.8
        self.invert_seek = False
        self.flip_pxy = False

        self.wavidx = 0
        self.snap_effect_emit = 0
        self.iframes = 0
        SnapEnemy.set_combat_vars(self)

        self.hp = 250
        

    def tick(self):
        if self.triggered:
            self.floor.add_fog(self, 0.5)

        y = self.floor.player.p[0] - self.p[0]
        x = self.floor.player.p[1] - self.p[1]

        md = (x*x)+(y*y)
        if( md < 250 ):
            if not self.triggered:
                self.triggered = True
                if not self.can_see_player():
                    self.triggered = False

        if not self.triggered:
            if(self.hp < 0):
                SnapEnemy.die(self)
                return False
            return True

        self.stimer = self.stimer + 1

        fridx = int( (self.stimer % 80) / 40)
        self.texture = Stork.textures[fridx]

        SnapEnemy.tick(self)

        if(self.state == Stork.STATE_WAITING):
            if(self.stimer==100):
                KSounds.play(KSounds.lifting_off)

            if self.stimer > 120:
                self.target_p = list(self.floor.player.p)
                self.stimer = 0
                self.state = Stork.STATE_LEAPING
                self.physics_suspended = True
                self.floor.snap_enemies.remove(self)

        if(self.state == Stork.STATE_LEAPING):
            self.fire_idx = 0
            self.texture = Stork.textures[2]
            self.p[1] = self.p[1] - 0.5
            self.size[0] = self.size[0] + 0.5
            self.size[1] = self.size[1] + 0.5
            if(self.stimer > 60):
                self.stimer = 0
                self.state = Stork.STATE_LANDING

        if(self.state == Stork.STATE_LANDING):
            self.size = [ 4, 4 ]
            self.texture = Stork.textures[2]
            dx = self.target_p[0] - self.p[0]
            dy = self.target_p[1] - self.p[1]

            self.p[0] = self.p[0] + (dx*0.2)
            self.p[1] = self.p[1] + (dy*0.2)


            if(self.stimer>40):
                self.p[0] = self.target_p[0]
                self.p[1] = self.target_p[1]
                self.physics_suspended = False
                if not self in self.floor.snap_enemies:
                    self.floor.snap_enemies.append(self)
                if(self.stimer % 15 == 0):
                    self.fire_circle()
                    self.fire_idx = self.fire_idx + 1
                if(self.stimer>(40+(15*3))):
                    self.stimer = 0
                    self.state = Stork.STATE_WAITING

        if(self.hp < 0):
            SnapEnemy.die(self)
            return False
        return True

    def fire_circle(self):
        num_shots = 3
        rad = (pi*2)/num_shots
        KSounds.play_eproj()
        #for x in range(0,num_shots):
        #    self.floor.create_object( ERangedMagic( p = [ self.p[0], self.p[1] ], rad = rad * x ) )
        x = self.fire_idx
        self.floor.create_object( ERangedMagic( p = [ self.p[0], self.p[1] ], rad = rad * x ) )
        


class Cleric(SnapEnemy):
    textures = [
        BGL.assets.get("KT-forest/texture/cleric0000"),
        BGL.assets.get("KT-forest/texture/cleric0001"),
        BGL.assets.get("KT-forest/texture/cleric0002")
    ]

    def receive_snap_attack(self, was_crit):
        SnapEnemy.receive_snap_attack(self, was_crit)

        if not was_crit:
            if not choice([True,False,False]):
                return                

        secondaries = []
        if self.floor.recursive_snapper is None:
            self.floor.recursive_snapper = self #HACKKKKKK
        for se2 in self.floor.snap_enemies:
            if se2.snap_type == SnapEnemy.ENEMY and se2.triggered:
                if(se2 is not self and se2 is not self.floor.recursive_snapper):
                    secondaries.append(se2)

        
        for x in range(0,3):
            if(len(secondaries))==0:
                break
            se2 = choice(secondaries)
            se2.receive_snap_attack(True)
            secondaries.remove(se2)

        if self.floor.recursive_snapper is self:
            self.floor.recursive_snapper = None
                
                

    def parse(od,df):
        o = Cleric( p = [ od["x"],od["y"] ] )
        df.snap_enemies.append(o)
        return o

    def customize(self):
        self.triggered = False
        self.tick_type = Object.TickTypes.PURGING
        self.light_type = Object.LightTypes.NONE
        self.light_color = [0.0,1.0,0.0,1.0]
        self.light_radius = 25.0
        self.snap_type = SnapEnemy.ENEMY
        self.visible = True
        self.z_index = 1
        self.buftarget = "popup"
        self.texture = Cleric.textures[0]
        self.widx = int(uniform(0.0,20.0))
        self.size = [ 3.5, 3.5 ]
        self.physics = { "radius" : 0.35, "mass"   : 0.0005, "friction" : 0.0 }
        #self.state = Skeline.STATE_SEEKING_RANDOM
        self.stimer = 0
        self.rvx = None
        self.speed = 3.2
        self.rejects_snap_attack = False#not used yet

        self.snap_effect_emit = 0
        self.iframes = 0
        SnapEnemy.set_combat_vars(self)
        self.hp = 95
        self.player_samples = []

    def tick(self):
    
        if self.hp<=0:
            SnapEnemy.die(self)
            return False
            
        p = self.floor.player.p
        x = p[0] - self.p[0]
        y = p[1] - self.p[1]
    
        md=(x*x)+(y*y)

        if(md<250):
            self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
            if not self.triggered:
                KSounds.play(KSounds.cleric_triggered)
            self.triggered = True 
        if(md>300):
            self.light_type = Object.LightTypes.NONE
            self.triggered = False

        self.widx = (self.widx + 1) % 20
        self.texture = Cleric.textures[floor(self.widx/10)]

        if self.triggered:
            if (choice([True,False,False,False]) and (self.stimer%30==0)) or (len(self.player_samples)==0):
                self.player_samples.append([self.floor.player.p[0],self.floor.player.p[1]])
                self.player_samples = self.player_samples[-5:]
                
            self.stimer = self.stimer + 1

            if(self.stimer>50):
                self.texture = Cleric.textures[2]
                self.light_color = [0.7+uniform(0.0,0.3),uniform(0.0,0.5),0.0,1.0]
                self.light_radius *= 0.98
                self.light_radius += uniform(0.1,0.6)
                if(self.stimer==55):
                    KSounds.play(KSounds.cleric_charge)
                if(self.stimer==60):
                    self.v = [ uniform(-2.0,2.0), uniform(-2.0,2.0) ]
                self.rejects_snap_attack = True

            if(self.stimer>100):
                self.rejects_snap_attack = False
                self.texture = Cleric.textures[2]
                self.light_color = [0.7+uniform(0.0,0.3),uniform(0.0,0.5),0.0,1.0]
                self.light_radius *= 1.1
                self.pickTarget()
                self.v = [0.0,0.0]
            if(self.stimer>120):
                if(self.stimer%8==1):
                    if(choice([True,True,False])):
                        self.fireRanged()
                        self.target_rad += uniform(0.5,1.5)
            if(self.stimer>160):
                self.stimer = 0
                self.light_color = [0.0,1.0,0.0,1.0]
                self.light_radius = 25.0
                self.v = [ uniform(-2.0,2.0), uniform(-2.0,2.0) ]

        return True

    def fireRanged(self):
        self.floor.create_object( ERangedMagic( p = [ self.p[0], self.p[1] ], rad = self.target_rad+uniform(-0.1,0.1) ) )
        KSounds.play_eproj()

    def pickTarget(self):
        
        x = self.floor.player.p[0] - self.p[0]
        y = self.floor.player.p[1] - self.p[1]
        rad = atan2(y,x)
        self.target_rad = rad - uniform(0.0,1.0)
    
class Skeline(SnapEnemy):
    def receive_snap_attack(self, was_crit):
        SnapEnemy.receive_snap_attack(self, was_crit)
        self.stimer = -10
        self.state = Skeline.STATE_SEEKING_RANDOM

    def parse(od,df):
        o = Skeline( p = [ od["x"],od["y"] ] )
        df.snap_enemies.append(o)
        return o

    STATE_SEEKING_RANDOM = 0
    STATE_SEEKING_PLAYER = 1
    STATE_CHARGING_SHOT = 2
    STATE_FIRING_SHOT = 3

    textures = [
        BGL.assets.get("KT-forest/texture/skeline0000"),
        BGL.assets.get("KT-forest/texture/skeline0001"),
        BGL.assets.get("KT-forest/texture/skeline0002"),
        BGL.assets.get("KT-forest/texture/skeline0003"),
    ] 
    def customize(self):
        self.triggered = False
        self.tick_type = Object.TickTypes.PURGING
        self.snap_type = SnapEnemy.ENEMY
        self.visible = True
        self.z_index = 1
        self.buftarget = "popup"
        self.texture = Skeline.textures[0]
        self.widx = int(uniform(0.0,40.0))
        self.size = [ 2.5, 2.5 ]
        self.physics = { "radius" : 0.35, "mass"   : 0.0005, "friction" : 0.0 }
        self.state = choice( [ Skeline.STATE_SEEKING_RANDOM, Skeline.STATE_SEEKING_PLAYER ] )
        #self.state = Skeline.STATE_SEEKING_RANDOM
        self.stimer = 0
        self.rvx = None
        self.speed = 3.8
        self.invert_seek = False
        self.flip_pxy = False

        self.snap_effect_emit = 0
        self.iframes = 0
        SnapEnemy.set_combat_vars(self)
        self.hp = 50
        

    def tick(self):
        if self.triggered:
            self.floor.add_fog(self, 0.30)
        SnapEnemy.tick(self)
        self.widx = (self.widx + 1) % 40
        self.wfr = floor(self.widx/20)
        self.texture = Skeline.textures[self.wfr]
        self.light_type = Object.LightTypes.NONE

        y = self.floor.player.p[0] - self.p[0]
        x = self.floor.player.p[1] - self.p[1]

        md = (x*x)+(y*y)
        if( md < 250 ):
            if not self.triggered:
                self.triggered = True
                test_segment = [ [ self.floor.player.p[0], self.floor.player.p[1] ], [self.p[0], self.p[1] ] ]
                for segment in self.floor.get_light_occluders():
                    if segments_intersect( segment, test_segment ):
                        self.triggered = False
                        break 
        if( md > 300 ):
            self.triggered = False

        if not self.triggered:
            if(self.hp < 0):
                SnapEnemy.die(self)
                return False
            #self.visible = False
            return True

        self.visible = True

        self.stimer = self.stimer + 1

        if self.invert_seek:
            calc_speed = self.speed * -0.4
        else:
            calc_speed = self.speed * 1.2

        if self.state == Skeline.STATE_SEEKING_PLAYER:

            ### hack acolyte seek
            p = self.floor.player.p
            pscore = abs(p[0] - self.p[0]) + abs(p[1]-self.p[1])
            for enemy in self.floor.snap_enemies:
                if not self.invert_seek and "is_acolyte" in enemy.__dict__ and enemy.triggered:
                    apscore = abs(enemy.p[0] - self.p[0]) + abs(enemy.p[1]-self.p[1])
                    if apscore<pscore:
                        p=enemy.p
                        break
        
                        

            self.rvx = None
            if self.flip_pxy:
                y = p[0] - self.p[0]
                x = p[1] - self.p[1]
            else:
                x = p[0] - self.p[0]
                y = p[1] - self.p[1]
    


            rad = atan2(y,x)
            vx = cos(rad) * calc_speed
            vy = sin(rad) * calc_speed
            self.v = [ vx,vy]

            if(self.stimer > 12 ):
                self.stimer = 0
                self.state = choice( [ Skeline.STATE_SEEKING_RANDOM, Skeline.STATE_SEEKING_PLAYER, Skeline.STATE_SEEKING_PLAYER ] )
                self.invert_seek = choice( [ False, True, False ] )
                if( self.state == Skeline.STATE_SEEKING_RANDOM ):
                    self.state = choice( [ Skeline.STATE_SEEKING_RANDOM, Skeline.STATE_CHARGING_SHOT, Skeline.STATE_SEEKING_PLAYER ] )
                    self.flip_pxy = choice( [ True, True, True, False ] )
        if self.state == Skeline.STATE_SEEKING_RANDOM:
            if not self.rvx:
                self.rvx = [ uniform(-1.0,1.0), uniform(-1.0,1.0) ]
                self.flip_pxy = choice( [ True, False ] )
            self.v = [ self.rvx[0] * calc_speed, self.rvx[1] * calc_speed ]
            if(self.stimer > 5 ):
                self.stimer = 0
                self.state = choice( [ Skeline.STATE_SEEKING_RANDOM, Skeline.STATE_SEEKING_PLAYER, Skeline.STATE_CHARGING_SHOT ] )
                self.invert_seek = choice( [ True, False ] )
        if self.state == Skeline.STATE_CHARGING_SHOT:
            if(self.stimer==1):
                KSounds.play(KSounds.charging_projectile)
            self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
            self.light_color = [1.0,0.4,0.1,1.0]
            self.light_radius = uniform(10.0,20.0)
            self.v = [0.0,0.0]
            self.texture = Skeline.textures[2]
            self.floor.create_object( Flare( p = [ self.p[0], self.p[1] ] ) )
            if( self.stimer > 20 ):
                self.stimer = 0
                self.state = Skeline.STATE_FIRING_SHOT
                self.pickTarget()
        if self.state == Skeline.STATE_FIRING_SHOT:
            self.texture = Skeline.textures[3]
            if( self.stimer > 15 ):
                self.state = Skeline.STATE_SEEKING_PLAYER
                self.fireRanged()

        if(self.hp < 0):
            SnapEnemy.die(self)
            return False

        return True

    def pickTarget(self):
        x = (self.floor.player.p[0] - self.p[0])+self.floor.player.v[0]
        y = (self.floor.player.p[1] - self.p[1])+self.floor.player.v[1]
        rad = atan2(y,x)
        self.target_rad = rad
        
    def fireRanged(self):
        #x = self.floor.player.p[0] - self.p[0]
        #y = self.floor.player.p[1] - self.p[1]
        #rad = atan2(y,x)
        self.floor.create_object( ERangedMagic( p = [ self.p[0], self.p[1] ], rad = self.target_rad ) )
        KSounds.play_eproj()

    def get_shader_params(self):
        bp = Object.get_shader_params(self)
        bp['translation_local'][0] = 0.1
        bp['translation_local'][1] = -0.4
        return bp
    
class Flare(Object):
    texture = BGL.assets.get('NL-lights/texture/flare')
    def customize(self):
        self.tick_type = Object.TickTypes.PURGING
        self.texture = Flare.texture
        self.size = [0.1,0.1]
        self.ttl = 90
        self.rp = uniform(-0.1,0.1)
        self.xp = uniform(1.01,1.08)
        self.light_type = Object.LightTypes.DYNAMIC_TEXTURE_OVERLAY
        self.visible = False
        self.buftarget = "floor"
        self.z_index = 100

    def tick(self):
        #self.light_color[3] = self.light_color[3] * uniform(0.7,0.9)
        #self.color[3] = self.color[3] * uniform(0.7,0.9)
        self.rad = self.rad + self.rp
        self.light_radius = uniform(10.0,80.0)

        self.size[0] = self.size[0]*self.xp
        self.size[1] = self.size[1]*self.xp
        self.ttl = self.ttl - 1
        if(self.ttl<0):
            self.floor.objects.remove(self)
            return False

        return True


class Splat(Object):
    textures = [
        BGL.assets.get('KT-forest/texture/splat0000'),
        BGL.assets.get('KT-forest/texture/splat0001'),
        BGL.assets.get('KT-forest/texture/splat0002'),
        BGL.assets.get('KT-forest/texture/splat0003'),
    ]
    def customize(self):
        self.tick_type = Object.TickTypes.PURGING
        self.cooldown = 80
        self.rad = uniform(-3.14,3.14)
        self.buftarget = "popup"
        self.zindex = 100
        self.size = [ uniform(1.3,2.7), uniform(1.3,2.7) ]
        self.spin = uniform(-0.1,0.1)

    def get_shader_params(self):
        sp = Object.get_shader_params(self)
        sp["filter_color"] = [1.0,1.0,1.0,float(self.cooldown)/80.]
        return sp

    def tick(self):
        self.floor.add_fog( self, 0.1 )
        self.size[0] = self.size[0] * 1.2 
        self.size[1] = self.size[1] * 1.2 
        self.rad = self.rad + self.spin
        self.cooldown = self.cooldown - 4.0
        if(self.cooldown<=0):
            self.floor.objects.remove(self)
            return False
        else:
            self.texture = Splat.textures[int(floor((80-self.cooldown) / 80)) ]
            return True

class Worm(SnapEnemy):
   
    textures = [
        BGL.assets.get("KT-forest/texture/worm0000"),
        BGL.assets.get("KT-forest/texture/worm0001"),
        BGL.assets.get("KT-forest/texture/worm0002"),
        BGL.assets.get("KT-forest/texture/worm0003"),
    ] 
    def get_kill_particles(self):
        return 5

    def customize(self):
        self.triggered = False
        self.hp = 5 + choice(range(0,30))
        self.dead = False
        self.tick_type = Object.TickTypes.PURGING
        self.fridx = choice(range(0,480))
        self.worm_target = None
        self.physics = { "radius" : 0.5, "mass"   : 0.0003, "friction" : 0.0 }
        self.fworm_target = [0.0,0.0]
        self.next_choice = 90
        self.buftarget = "popup"
        self.size = [1.2,1.2]
        self.attacking = False
        self.z_index = 1
        self.biting = False
        self.snap_type = SnapEnemy.ENEMY
        self.iframes = 0
        self.defense = 3
        self.lifetime = 0
        
    def pick_target(self):
        rad = None
        speed = None
        if hypot(self.p[0]-self.floor.player.p[0], self.p[1]-self.floor.player.p[1]) < 10.0:
            x = self.floor.player.p[0] - self.p[0]
            y = self.floor.player.p[1] - self.p[1]
            rad = atan2(-1*y,x)
            speed = uniform(4.0,10.0)
            self.attacking = True
        else:
            rad = uniform(-3.14,3.14)
            speed = uniform(0.2,1.3)
            self.attacking = False

        if(uniform(0.0,1.0)>0.06):
            self.worm_target = [ cos(rad)*speed, -1*sin(rad)*speed ]
        else:
            self.worm_target = [ cos(-1*rad)*speed, -1*sin(-1*rad)*speed ]

        self.next_choice = 2

    def should_draw(self):
        p = self.get_shader_params()['translation_world']
        visRad = vconf.visRad
        if(p[0]<-visRad): return False
        if(p[1]<-visRad): return False
        if(p[0]>visRad): return False
        if(p[1]>visRad): return False
        return True

    def tick(self):

        self.lifetime+=1
        if(self.lifetime>10):
            self.triggered = True
        if(self.floor.player.kill_success):
            return True

        if(self.dead):
            self.color = [0.0,0.0,0.0,1.0]
            self.buftarget="floor"
            return True

        if(uniform(0.0,1.0)>0.6):
            return True

        if not self.should_draw():
            return True

        self.rad = atan2( self.fworm_target[1], self.fworm_target[0] )
        self.fridx = self.fridx + 1

        if self.attacking:
            tidx = int(self.fridx/15)%4
        else:
            tidx = int(self.fridx/24)%4

        self.texture = Worm.textures[tidx]

        if(not self.worm_target):
            self.pick_target()
        elif (self.fridx%self.next_choice) == 0:
            self.pick_target()

        freq = 20
        self.biting = False
        if self.attacking:
            freq = 5
        if(self.fridx%freq)==0:
            self.fworm_target[0] = (self.fworm_target[0]*0.8) + (self.worm_target[0]*0.2)
            self.fworm_target[1] = (self.fworm_target[1]*0.8) + (self.worm_target[1]*0.2)

            if self.attacking: 
                if tidx == 3: 
                    self.biting = True

        rsize = self.size
        if(tidx>2):
            rsize = [1.6,1.6]
        elif(tidx==0):
            rsize = [1.4,1.4]
        elif(tidx==1):
            rsize = [1.1,1.1]

        self.size[0] = (self.size[0] *0.7) + (rsize[0]*0.3)
        self.size[1] = (self.size[1] *0.7) + (rsize[1]*0.3)
        self.v[0] = self.fworm_target[0] * (float((tidx)+0.1)*0.25)
        self.v[1] = self.fworm_target[1] * (float((tidx)+0.1)*0.25)


        self.color = [1.0,1.0,1.0,1.0]
        self.light_type = Object.LightTypes.NONE
        if self.attacking:
            self.color = [uniform(0.5,1.0),uniform(0.0,1.0),0.0,1.0]
        if self.biting:
            self.v[0] = self.v[0]*4
            self.v[1] = self.v[1]*4
            self.color = [0.0,1.0,0.0,1.0]
            self.light_color = [uniform(0.0,1.0),uniform(0.0,1.0),0.0,1.0]
            self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
            self.light_radius = uniform(10.0,20.0)

            if hypot(self.floor.player.p[0] - self.p[0], self.floor.player.p[1] - self.p[1] ) < 2.0:
                self.floor.player.enemy_attack(3)

        if (not self.biting):
            if hypot(self.floor.player.p[0] - self.p[0], self.floor.player.p[1] - self.p[1] ) < 7.0:
                if(self.floor.player.sword.state == Sword.STATE_DISCHARGING) or (self.floor.player.sword.state == Sword.STATE_SPIN_ATTACK):
                    self.hp -= 1.5
                    self.floor.player.notify_succesful_attack()
                    self.floor.player.next_dashcombo()
                    self.v[0] = self.v[0]*-8
                    self.v[1] = self.v[1]*-8
                    self.floor.create_object( Splat( p = self.p ) )

        if(self.hp<0.0):
            SnapEnemy.die(self)
            for fi in range(0,3):
                self.floor.create_object( Flare( p = [ self.p[0], self.p[1] ] ) )
            return False

        return True
    
        
class WormField(Object):
    def customize(self):
        self.tick_type = Object.TickTypes.PURGING
        self.buftarget = "popup"
        self.visible = False

        self.p[0] = self.wf_spec[0]
        self.p[1] = self.wf_spec[1]
        self.wf_radius = self.wf_spec[2]
        self.worms = []

    def tick(self):
        if(len(self.worms)<13):
            worm = Worm( p = [self.p[0],self.p[1] ] )
            self.worms.append(worm)
            self.floor.snap_enemies.append(worm)
            self.floor.create_object(worm)
            return True
        return False


class Elder(Object):
    #texture = BGL.assets.get('KT-player/texture/elder0000')
    texture = BGL.assets.get('KT-forest/texture/cave_entrance')

    def customize(self):
        self.texture = Elder.texture
        #self.buftarget = "popup"
        self.buftarget = "floor"
        self.size =  [ 20.0, 20.0 ]
        self.light_type = Object.LightTypes.STATIC_SHADOWCASTER
        self.light_color =  [ 0.0,0.0,1.0,1.0]
        #self.physics = { "radius" : 1.0, "mass"   : 100.0, "friction" : 0.0 } 
        self.tick_type = Object.TickTypes.TICK_FOREVER
        self.z_index = 1

    def tick(self):
        dx = self.p[0] - self.floor.player.p[0]
        dy = self.p[1] - self.floor.player.p[1]

        dst = (dx*dx+dy*dy)

        if(dst<30):
            self.floor.player.set_hud_message("{x} => talk")
            if self.floor.player.get_pad().button_down( BGL.gamepads.buttons.X ):
                pass

class Totem(Object):
    texture = BGL.assets.get('KT-forest/texture/totem')

    def customize(self):
        self.snap_type = SnapEnemy.TOTEM
        self.texture = Totem.texture
        self.buftarget = "popup"
        self.size =  [ 4.0, 4.0 ]
        self.tick_type = Object.TickTypes.TICK_FOREVER
        self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
        self.light_color =  [ 0.7,0.4,0.9,1.0]
        self.light_radius = 5
        #self.physics = { "radius" : 1.0, "mass"   : 100.0, "friction" : 0.0 } 
        self.physics = None
        self.z_index = 1
        self.anim_index = 0
        self.reset_timer = 0

    def tick(self):
        self.reset_timer = self.reset_timer+1
        if(self.reset_timer == - 50):
            KSounds.play(KSounds.totem_restored)
        if(self.reset_timer==0):
            self.floor.snap_enemies.append(self)
            self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
            self.light_radius = 17
            self.visible = True
        self.anim_index += 0.1
        self.light_radius = 7 + (3*sin(self.anim_index))

    def sleep_totem(self):
        KSounds.play(KSounds.totem_hit)
        self.floor.snap_enemies.remove(self)
        self.reset_timer = -170
        self.visible = False
        self.light_type = Object.LightTypes.NONE

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

class SwordCrit(Object):
    texture = BGL.assets.get('KT-player/texture/sword')

    def customize(self):
        self.texture = SwordCrit.texture
        self.buftarget = "hud"

        self.size =  [ 9.0, 9.0 ]
        self.rad = 3.14/2
        #self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
        self.light_type = Object.LightTypes.NONE
        self.light_color =  [ 0.0,1.0,0.0,1.0]
        self.color = [ 1.0,1.0,1.0,0.5]
        self.light_radius = 50.0
        self.physics = None
        self.z_index = 9000
        self.tick_type = Object.TickTypes.PURGING
        self.delta_vy = 0.3
        self.lifetime = 0
        self.delay = 0
        self.visible = False
        self.anim_tick = 0.2

    def tick(self):

        if(self.delay> 5):
            self.visible = True
            self.lifetime = self.lifetime + 1
            self.p[1] = self.p[1] + self.delta_vy
            self.delta_vy *= 1.2

            self.anim_tick = self.anim_tick * 1.08
            if(self.lifetime > 30):
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

            dx = self.p[0] - self.floor.camera.p[0]
            dy = self.p[1] - self.floor.camera.p[1]
            md = (dx*dx)+(dy*dy)
            impulse_a = self.draw_color[3]
            if(md < 190):
                impulse_a = 0.0

            self.last_a = (self.last_a * 0.9) + (impulse_a*0.1)
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

            if od["key"] in [ "snap_enemy", "skeline"]:
                self.objects.append(Skeline.parse(od,df ))

            if od["key"] in [ "cleric"]:
                self.objects.append(Cleric.parse(od,df ))

            if od["key"] in [ "acolyte" ]:
                self.objects.append(Acolyte.parse(od,df ))

            if od["key"] in [ "stork" ]:
                self.objects.append(Stork.parse(od,df ))



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

                if uniform(0.0,1.0) < 0.8:
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
