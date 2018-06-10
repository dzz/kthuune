from Beagle import API as BGL
from Newfoundland.Object import Object
from math import sin,cos,atan2, tanh
from random import choice
from ..LevelEffects.SwordCrit import SwordCrit


class SlashEffect(Object):
    textures = [
        BGL.assets.get('KT-player/texture/sword'),
        BGL.assets.get('KT-player/texture/sword'),
        BGL.assets.get('KT-player/texture/sword'),
    ]

    def customize(self):
        self.buftarget = "popup"
        self.size = [1.5,1.5]
        self.tick_type = Object.TickTypes.TICK_FOREVER
        self.light_type = Object.LightTypes.NONE
        self.light_radius = 7.0
        self.light_color = [1.0,1.0,1.0,1.0]
        self.fr = 0
        self.visible = False
        self.texture = SlashEffect.textures[0]
        self.z_index = -1
        self.cooldown = 0
        self.stagger_cooldown = 0
        self.base_extension = 0.6
        self.extension = 0.0
        self.alpha = 0.0
        self.snapped_v = ( 0.0,1.0)
        self.ext_delta = 0.0
        self.base_reg = 1.2

    def slash(self):
        self.alpha = 1.0
        if(self.floor.player.run_stamina>0):
            self.floor.player.sword_swing = self.floor.player.sword_swing_cooldown
            if(self.cooldown>0):
                return False
            self.texture = SlashEffect.textures[0]
            self.fr = 0
            self.visible = True

            pad = self.floor.player.controllers.get_virtualized_pad(0)

            self.rad = atan2( pad.left_stick[1], pad.left_stick[0]) + (3.14/2)
            self.snapped_v = ( sin(self.rad), -1*cos(self.rad) ) 
            self.extension = 0
            self.ext_delta = 0.44

            self.orig_rad = self.rad
            self.floor.player.sword.visible = False
            self.attacked_enemies = []
            self.cooldown = 41 
            self.stagger_cooldown = 4
            self.floor.sounds.play( self.floor.sounds.slash )
            self.floor.player.run_stamina -= 20
            self.floor.player.total_slashes += 1

            self.base_extension = 1.2
            self.p[0] = self.floor.player.p[0]
            self.p[1] = self.floor.player.p[1] 
            return True

    def tick(self):
        self.ext_delta *= 0.92
        self.extension += self.ext_delta

        if(self.ext_delta > 0) and (self.extension>5.0):
            self.ext_delta *= -1
        if(self.extension<0.0):
            self.ext_delta = 0.0

        if(self.cooldown>0):
            self.cooldown -= 1

        cutoff = 0.2
        decay = 0.88
        self.snapped_v = ( self.snapped_v[0] *decay , self.snapped_v[1] *decay )

        pad = self.floor.player.controllers.get_virtualized_pad(0)

        if(abs(self.snapped_v[0])+abs(self.snapped_v[1]))<cutoff:
            cfa,cfb = 0.8,0.2
            self.p[0] = (self.p[0] * cfa) + (self.floor.player.p[0] * cfb)
            self.p[1] = (self.p[1] * cfa) + (self.floor.player.p[1] * cfb)
        else:
            def expmod(v):
                return tanh(v)

            pcf = 0.12
            damp = 0.8
            self.p[0] = self.p[0] + ((self.snapped_v[0] +  (expmod(self.floor.player.v[0]*pcf)) )*damp)
            self.p[1] = self.p[1] + ((self.snapped_v[1] +  (expmod(self.floor.player.v[1]*pcf)) )*damp)


        if self.stagger_cooldown==0:
            self.rad=self.rad-(3.14/17)
            self.alpha *= 0.95
            self.base_extension += 0.14

        Object.light_type = Object.LightTypes.NONE

        if self.visible:
            self.flash_color[3]*=0.9
            Object.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER

            if self.fr == 3:
                self.flash_color = [1.0,0.5,0.0,1.0]

            if self.fr>2 and self.fr < 19 and (self.stagger_cooldown==0):
                for enemy in self.floor.snap_enemies:
                    if enemy.snap_type==1 and enemy not in self.attacked_enemies and len(self.attacked_enemies)<3:
                        dx = self.p[0] - enemy.p[0] 
                        dy = self.p[1] - enemy.p[1] 
                        md = (dx*dx) + (dy*dy)
                        if md < ((enemy.physics["radius"]*enemy.physics["radius"])+6.0):
                            self.floor.player.v[0] = -1*dx*0.3
                            self.floor.player.v[1] = -1*dy*0.3
                            #self.floor.player.p[0] = enemy.p[0]
                            #self.floor.player.p[1] = enemy.p[1]
                            self.floor.sounds.play( self.floor.sounds.slashhit )
                            #enemy.floor.player.add_dm_message("You slashed an enemy")

                            self.snapped_v = (0.0,0.0)
                            if(self.floor.player.running):
                                enemy.receive_snap_attack( choice([True,False]) )
                            else:
                                enemy.receive_snap_attack( choice([False, False, True]) )
                            self.attacked_enemies.append(enemy)
                            self.stagger_cooldown += 7
                            self.floor.create_object( SwordCrit( p = [ self.p[0], self.p[1]-15 ]))
            if self.stagger_cooldown==0:
                self.fr+=1 

                if self.fr >14:
                    if self.floor.player.A_STATE[1] == False:
                        self.fr = 20
                        self.visible = False
            else: 
                self.stagger_cooldown -=1
            if self.fr == 120:
                self.stagger_cooldown = 0
                self.visible = False
                self.attacked_enemies = []
                self.floor.player.sword.visible = True
                return
            self.texture = SlashEffect.textures[0]
            

    def get_guppy_batch(self):
        batch = [ self.get_shader_params() ]

        batch[0]["rotation_local"] = -1.5705
        batch[0]["translation_world"][1] -= 0.7

        return batch
        
