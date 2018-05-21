from Beagle import API as BGL
from Newfoundland.Object import Object
from math import sin,cos
from random import choice

class SlashEffect(Object):
    textures = [
        BGL.assets.get('KT-player/texture/slash0000'),
        BGL.assets.get('KT-player/texture/slash0001'),
        BGL.assets.get('KT-player/texture/slash0002'),
    ]

    def customize(self):
        self.buftarget = "popup"
        self.size = [2.5,2.5]
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
        self.alpha = 0.0


    def slash(self):
        self.alpha = 1.0
        if(self.floor.player.run_stamina>0):
            self.floor.player.sword_swing = self.floor.player.sword_swing_cooldown
            if(self.cooldown>0):
                return
            self.texture = SlashEffect.textures[0]
            self.fr = 0
            self.visible = True
            self.rad = self.floor.player.rad
            self.orig_rad = self.rad
            self.floor.player.sword.visible = False
            self.attacked_enemies = []
            self.cooldown = 41 
            self.stagger_cooldown = 0
            self.floor.sounds.play( self.floor.sounds.slash )
            self.floor.player.run_stamina -= 20
            self.floor.player.total_slashes += 1

            self.base_extension = 0.6

    def tick(self):


        if(self.cooldown>0):
            self.cooldown -= 1

        offsx = ((cos(self.rad)*2.0)+(self.floor.player.v[0]*0.4))*0.5
        offsy = ((sin(self.rad)*2.0)+(self.floor.player.v[1]*0.4))*0.5

        if self.stagger_cooldown==0:
            self.rad=(self.rad*0.8)+(self.floor.player.rad*0.2)
            self.alpha *= 0.9

        self.p[0] = self.floor.player.p[0] + offsx
        self.p[1] = self.floor.player.p[1] + offsy

        Object.light_type = Object.LightTypes.NONE
        if self.visible:
            Object.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
            if self.fr>3 and self.fr < 19 and (self.stagger_cooldown==0):
                for enemy in self.floor.snap_enemies:
                    if enemy.snap_type==1 and enemy not in self.attacked_enemies and len(self.attacked_enemies)<3:
                        dx = self.p[0] - enemy.p[0] 
                        dy = self.p[1] - enemy.p[1] 
                        md = (dx*dx) + (dy*dy)
                        if md < ((enemy.physics["radius"]*enemy.physics["radius"])+4.0):
                            self.floor.player.v[0] = -1*dx*0.3
                            self.floor.player.v[1] = -1*dy*0.3
                            #self.floor.player.p[0] = enemy.p[0]
                            #self.floor.player.p[1] = enemy.p[1]
                            self.floor.sounds.play( self.floor.sounds.slashhit )
                            #enemy.floor.player.add_dm_message("You slashed an enemy")
                            if(self.floor.player.running):
                                enemy.receive_snap_attack( choice([True,False]) )
                            else:
                                enemy.receive_snap_attack( choice([False, False, True]) )
                            self.attacked_enemies.append(enemy)
                            self.stagger_cooldown += 7
            if self.stagger_cooldown==0:
                self.fr+=1 

                if self.fr >14:
                    if self.floor.player.A_STATE[1] == False:
                        self.fr = 20
                        self.visible = False
            else: 
                self.stagger_cooldown -=1
            if self.fr == 21:
                self.stagger_cooldown = 0
                self.visible = False
                self.attacked_enemies = []
                self.floor.player.sword.visible = True
                return
            self.texture = SlashEffect.textures[ self.fr//7 ]
            

    def get_guppy_batch(self):
        batch = [ Object.get_shader_params(self), self.get_shader_params() ]

        batch[0]["texBuffer"]=BGL.assets.get("KT-forest/texture/registration2")
        batch[0]["rotation_local"] = 0.0
        batch[0]["scale_local"] = [ 2.0,2.0]
        batch[0]["filter_color"][3] = self.alpha

        return batch
        
