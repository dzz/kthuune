from Newfoundland.Object import Object
from Beagle import API as BGL

class TumorCrab(Object):
    textures = BGL.assets.get('KT-forest/animation/tumorcrab')

    def parse(od,df):
        tc = TumorCrab(p=[od["x"],od["y"]])
        return tc

    def customize(self):
        self.visible = True
        self.buftarget = "popup"
        self.z_index = 500
        self.size = [20,20]
        self.texture = TumorCrab.textures[0]
        self.tick_type = Object.TickTypes.PURGING
        self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
        self.light_color = [ 1.0,0.5,0.5,1.0 ]
        self.light_radius = 200
        self.fr = 0.0
        self.color = [ 1.0,1.0,1.0,0.0 ]
        self.active = False
        self.life = 0.0

    def tick(self):
        if self.active:
            if(self.life<1.0):
                self.life += 0.01
            self.light_color = [ 1.0,uniform(0.5,0.9),uniform(0.3,0.7),1.0 ]
            self.light_radius = uniform(200,300)
            self.fr += 0.7
            if self.color[3] < 1.0:
                self.color[3] += 0.01
            if(self.fr> len(TumorCrab.textures)):
                self.fr = 0.0

            self.texture = TumorCrab.textures[ int(self.fr) ]

            self.p[1] -= 0.13*self.life
            if self.fr < 37:
                self.vy = 0.038*self.life
            if( self.fr > 37 ):
                self.p[1] -= self.vy
                self.vy*=1.047

            dy = self.floor.player.p[1] - self.p[1]
            dx = self.floor.player.p[0] - self.p[0]

            self.flash_color= [ 1.0,1.0,1.0,0.0]
            if(abs(dx)<8):
                if dy>0 and dy <10:
                    if uniform(0.0,1.0) > 0.4:
                        self.attack_str = 30
                        self.vx = 0
                        self.vy = 0
                        if self.floor.player.hp >0:
                            self.floor.player.receive_ranged_attack(self)

                if (self.fr>39 and self.fr<47) or (self.fr>80 or self.fr< 5):
                    self.flash_color= [ 1.0,1.0,0.0,1.0]
                    if dy> -17 and dy<-11:
                        self.attack_str = 30
                        self.vx = 0
                        self.vy = 0
                        if self.floor.player.hp >0:
                            self.floor.player.receive_ranged_attack(self)
            
        else:
            if(self.floor.player.p[1] - self.p[1] < -50 ):
                self.active = True
                self.floor.camera.grab_cinematic( self, 120 )
            return True
    
        return True
