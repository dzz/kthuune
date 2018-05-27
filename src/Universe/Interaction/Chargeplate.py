from Newfoundland.Object import Object
from Beagle import API as BGL
from math import floor, sin
from random import uniform, choice
from ..LevelProps.CableSegment import CableSegment

from ..LevelEffects.Poof import Poof
from ..LevelEffects.AttackInfo import AttackInfo
from ..Particles.SplatterParticle import SplatterParticle
from ..Particles.Bird import Bird
from ..LevelEffects.Explosion import Explosion

class Chargeplate(Object):
    PLATES = 0
    GENOCIDE = 1

    textures = BGL.assets.get('KT-forest/animation/chargeplate')

    def parse(od,df):
        o = Chargeplate( p = [ od["x"],od["y"] ] )

        o.group = 0
        if("group" in od["meta"]):
            o.group = od["meta"]["group"]

        if(o.group!=0):
            o.visible = False
            o.light_type = Object.LightTypes.NONE
        return o
        

    def generate_cable(self, floor):
        target = floor.get_owl_p( self.group )
        self.cable_segments = CableSegment.generate_cable( self.p[0], self.p[1], target[0], target[1] )
        return self.cable_segments

    def customize(self):
        #self.tooltip = "Stand on me!"
        self.size = [ 2.3, 2.3 ]
        self.buftarget = "popup"
        self.tick_type = Object.TickTypes.PURGING
        self.texture = Chargeplate.textures[0]
        self.color = [ 0.0,0.0,0.0,1.0 ]
        self.fr = 0.0
        self.cv = 0.0
        self.charged = False
        self.incr_frames = 0
        self.decr_frames = 0
        self.l_idx = 0
        self._t = 0
        self._t_offs = uniform(0.0,100.0)

    def tick(self):

        self._t += 0.1
        self.rad = sin( self._t + self._t_offs ) * 0.1
        if(self.visible):
            self.color = [
                1.0+self.cv,
                1.0+self.cv,
                1.0+self.cv,
                1.0 ]
            self.light_color = [ 1.0,1.0,self.cv ]
            self.light_radius = 2.0 + (self.cv*3.0)
            self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER

            self.flash_color[3] *= 0.98;
            
            if not self.charged:
                if( uniform(0.0,1.0)>0.98):
                    i = uniform(0.8,1.5)
                    self.flash_color = [ 0,0.0,i,1.0]

        if(not self.visible):
            return True

        if(self.charged):
            #self.tooltip = "I'm charged, find more of me!"
            self.flash_color[3] = 0.0 
            notify_timeout = 30

            check = True
            for chargeplate in self.floor.chargeplates:
                if chargeplate.group==self.group and chargeplate.charged == False:
                    check = False
                    break

            if check:
                if self.group in self.floor.group_to_owl:
    
                    owl = self.floor.group_to_owl[self.group]
                    self.floor.camera.grab_cinematic(owl,3,None)
                    owl.visible = False
                    self.floor.sounds.play( choice([ self.floor.sounds.enemy_killed, self.floor.sounds.enemy_killed2 ]) )
                    self.floor.create_object(Explosion(p=list(owl.p)))
                    for x in range(0,20):
                        spltr = SplatterParticle( p = list(owl.p), size = [ 5.0,5.0],rad = uniform(-3.14,3.14))
                        self.floor.create_object(spltr)
                    

                for chargeplate in self.floor.chargeplates:
                    if chargeplate.group == self.group + 1:
                        if not(chargeplate.visible):
                            dfloor = self.floor

                            def fnn(chargeplate):
                                cbplat = chargeplate
                                def nn():
                                    cbplat.visible = True
                                    ai = AttackInfo( p=[ cbplat.p[0], cbplat.p[1] ], message="~new node~")
                                    self.floor.camera.grab_cinematic( ai, 40 )
                                    self.floor.sounds.play(self.floor.sounds.sequenced)
                                    dfloor.create_object(ai)
                                return nn
                            self.floor.add_timeout( [ fnn(chargeplate), notify_timeout ] )
                            notify_timeout += 40

            self.floor.sounds.play(self.floor.sounds.charged)
            self.floor.player.pump_timer('chargeplate')

            self.texture = Chargeplate.textures[ len(Chargeplate.textures)-1]
            self.color = [ 1.0,1.0,1.0,1.0 ]
            win = True
            for cp in self.floor.chargeplates:
                if(not cp.charged):
                    win = False
                    break                    
            if win: 
                dfloor = self.floor
                def ns():
                    #dfloor.game.next_sequence()
                    dfloor.game_mode = Chargeplate.GENOCIDE
                    ai = AttackInfo( p=[ self.p[0], self.p[1]+3 ], message="~!PuRiFy!~")
                    self.floor.sounds.play(self.floor.sounds.sequenced)
                    dfloor.create_object(ai)

                def ms():
                    ai = AttackInfo( p=[ self.p[0], self.p[1] ], message="~SEQUENCED~")
                    self.floor.sounds.play(self.floor.sounds.sequenced)
                    dfloor.create_object(ai)

                self.floor.add_timeout( [ ms, 30 ] )
                self.floor.add_timeout( [ ns, 60 ] )
                #self.floor.game.trigger_fade( 242, [ 1.0,1.0,1.0] )
            return False

        self.fr += self.cv*0.1

        if(self.fr>= len (Chargeplate.textures)):
            self.fr = 0

        self.texture = Chargeplate.textures[floor(self.fr)]

        n_lidx = floor((self.cv * 8))

        if(n_lidx!=self.l_idx):
            self.floor.sounds.play(self.floor.sounds.charging)
            for cable in self.cable_segments:
                cable.flash_color = [ 1.0,1.0,1.0,1.0 ]
            if self.group in self.floor.group_to_owl:
                self.floor.group_to_owl[self.group].flash_color = [ 0.0,1.0,0.0,1.0]
        self.l_idx = n_lidx

        if(self.mdist( self.floor.player)<2.27):
            if self.group in self.floor.group_to_owl:
                self.floor.camera.grab_cinematic(self.floor.group_to_owl[self.group],1,None)

            self.cv += 0.03
            self.flash_color[3] = 0.0
            if( uniform(0.0,1.0) >  0.9 ):
                self.floor.create_object(Poof( p = list(self.p)))
                for x in range(0,1):
                    spltr = Bird( p = [self.p[0]+uniform(0.0,self.size[0]), self.p[1]+uniform(-4.0,4.0)])
                    spltr.color = [0.0,0.0,0.0,1.0]
                    spltr.light_color = [ 0.0,1.0,0.0,1.0]
                    spltr.size[0]*=uniform(1.0,1.5)
                    self.floor.create_object(spltr)
            #self.floor.objects.remove(self)
            #return False            
        else:
            self.cv *= 0.98

        if(self.cv>1.0):
            self.cv = 1.0
            self.charged = True
            self.floor.sounds.play( choice([ self.floor.sounds.enemy_killed, self.floor.sounds.enemy_killed2 ]) )
            for cable in self.cable_segments:
                cable.tick = lambda : False
                cable.visible = False
                spltr = Explosion( p = list(cable.p), rad = cable.rad )
                self.floor.create_object(spltr)
            self.floor.create_object(AttackInfo( p=[ self.p[0], self.p[1] ], message="~charged~"))

            for s in self.cable_segments:
                self.floor.simple_tick_manager.tickables.remove(s)
                s.flash_color = [ 1.0,1.0,1.0,1.0 ]

        return True

