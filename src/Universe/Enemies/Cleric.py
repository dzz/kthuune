from Newfoundland.Object import Object
from .SnapEnemy import SnapEnemy
from random import uniform, choice
from math import sin,cos,atan2,floor
from Beagle import API as BGL
from client.beagle.Newfoundland.GeometryUtils import segments_intersect
from ..LevelEffects.ChromaticWave import ChromaticWave
from ...KSounds import KSounds
from ..RangedEnemyAttacks.BasicProjectile import BasicProjectile
from ..LevelEffects.AttackInfo import AttackInfo
from ..LevelEffects.Explosion import Explosion

class Cleric(SnapEnemy):
    textures = [
        BGL.assets.get("KT-forest/texture/cleric0000"),
        BGL.assets.get("KT-forest/texture/cleric0001"),
        BGL.assets.get("KT-forest/texture/cleric0002")
    ]

    def skips_spawn(self):
        if(self.permadeath):
            return True
        key_group = self.group+1
        if key_group in self.floor.activated_totem_groups:
            self.permadeath = True
            return True
        return False

    def receive_snap_attack(self, was_crit):
        SnapEnemy.receive_snap_attack(self, was_crit)

        if not was_crit:
            if not choice([True,False,False]):
                return                

        #secondaries = []
        #if self.floor.recursive_snapper is None:
        #    self.floor.recursive_snapper = self #HACKKKKKK
        #for se2 in self.floor.snap_enemies:
        #    if se2.snap_type == SnapEnemy.ENEMY and se2.triggered:
        #        if(se2 is not self and se2 is not self.floor.recursive_snapper):
        #            secondaries.append(se2)

        #for x in range(0,3):
        #    if(len(secondaries))==0:
        #        break
        #    se2 = choice(secondaries)
        #    se2.receive_snap_attack(True)
        #    secondaries.remove(se2)

        #if self.floor.recursive_snapper is self:
        #    self.floor.recursive_snapper = None
                
                

    def parse(od,df):
        o = Cleric( p = [ od["x"],od["y"] ] )
        SnapEnemy.set_group(o,od)
        df.snap_enemies.append(o)
        df.enemies.append(o)
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
        self.permadeath = False
        self.snap_effect_emit = 0
        self.iframes = 0
        SnapEnemy.set_combat_vars(self)
        self.hp = 95
        self.player_samples = []

    def is_cleric(self):
        return True

    def custom_die(self):
        key_group = self.group+1
        if key_group in self.floor.activated_totem_groups:
            return
            
        for enemy in self.floor.enemies:
            notify_amt = 0
            if enemy.is_cleric():
                if enemy.hp>0:
                    if enemy.group == self.group:
                        return

        ai = AttackInfo( p=list(self.p), message="!BREAK!")
    
        self.floor.game.rb = 1.0

        self.floor.create_object(ai)

        garbage_spawners = []
        for spawner in self.floor.spawners:
            if spawner.loser.is_cleric():
                if spawner.loser.group == self.group:
                    garbage_spawners.append(spawner)

        for spawner in garbage_spawners:
            self.floor.remove_object(spawner)
            self.floor.purging_tick_manager.tickables.remove(spawner)
            self.floor.spawners.remove(spawner)

        self.floor.activated_totem_groups.append(key_group)
        for totem in self.floor.totems:
            if totem.group == key_group:
                def fns(totem):
                    def ns():
                        ai = AttackInfo( p=list(totem.p), message="~connection~")
                        self.floor.camera.grab_cinematic( ai, 40 )
                    return ns
                     
                totem.active = True
                totem.reset_timer = -51
                self.floor.add_timeout([fns(totem), 50+notify_amt])
                notify_amt += 40
        target_group = self.group+1
        notify_timeout = 20
        for enemy in self.floor.enemies:
            if not enemy.is_cleric():
                continue
            #print("CHECKING ENEMEY GROUP {0} == {1}",enemy.group, target_group )
            if enemy.group == target_group:
                def fes(enemy):
                    def es():
                        enemy.group_active = True
                        enemy.flash_color = [ 1.0,1.0,1.0, 1.0 ]
                        enemy.p[0] += 99999
                        enemy.p[1] += 99999
                        enemy.physics_suspended = False
                        enemy.tick()
                        enemy.visible = True
                        enemy.triggered = True
                        ai= AttackInfo( p=[ enemy.p[0], enemy.p[1] ], message="~mutation~")
                        self.floor.create_object( Explosion( p = list(enemy.p) ) )
                        self.floor.create_object(ai)
                        self.floor.camera.grab_cinematic( ai, 50 )
                        self.floor.sounds.play(self.floor.sounds.spawned)
                    return es

                self.floor.add_timeout( [fes(enemy), notify_timeout])
                notify_timeout += 50

    def tick(self):
        if(self.floor.player.title_card.displaying()):
            return True
        if(SnapEnemy.handle_tick_disabled(self)):
            return True

        self.fade_flash()

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
        self.flash(1.0,0.8,0.0)
        self.floor.create_object( BasicProjectile( p = [ self.p[0], self.p[1] ], rad = self.target_rad+uniform(-0.1,0.1) ) )
        KSounds.play_eproj()

    def pickTarget(self):
        
        x = self.floor.player.p[0] - self.p[0]
        y = self.floor.player.p[1] - self.p[1]
        rad = atan2(y,x)
        self.target_rad = rad - uniform(0.0,1.0)
