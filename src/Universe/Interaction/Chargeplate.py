from Newfoundland.Object import Object
from Beagle import API as BGL
from math import floor
from random import uniform, choice
from ..LevelProps.CableSegment import CableSegment

from ..LevelEffects.Poof import Poof
from ..LevelEffects.AttackInfo import AttackInfo

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
        return o
        

    def generate_cable(self, floor):
        target = floor.get_owl_p( self.group )
        self.cable_segments = CableSegment.generate_cable( self.p[0], self.p[1], target[0], target[1] )
        return self.cable_segments

    def customize(self):
        #self.tooltip = "Stand on me!"
        self.size = [ 2.0, 2.0 ]
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

    def tick(self):

        if(self.visible):
            self.color = [
                1.0+self.cv,
                1.0+self.cv,
                1.0+self.cv,
                1.0 ]
            self.light_color = [ 1.0,1.0,self.cv ]
            self.light_radius = 2.0 + (self.cv*3.0)
            self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER

            self.flash_color[3] *= 0.95;
            
            if not self.charged:
                if( uniform(0.0,1.0)>0.9):
                    i = uniform(0.8,1.5)
                    self.flash_color = [ 0,0,i,1.0]

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

        self.fr += self.cv

        if(self.fr>= len (Chargeplate.textures)):
            self.fr = 0

        self.texture = Chargeplate.textures[floor(self.fr)]

        n_lidx = floor((self.cv * 8))

        if(n_lidx!=self.l_idx):
            self.floor.sounds.play(self.floor.sounds.charging)
            for cable in self.cable_segments:
                cable.flash_color = [ 1.0,1.0,1.0,1.0 ]
        self.l_idx = n_lidx



        if(self.mdist( self.floor.player)<2.27):
            self.cv += 0.03
            self.flash_color[3] = 0.0
            self.floor.create_object(Poof( p = list(self.p)))
            #self.floor.objects.remove(self)
            #return False            
        else:
            self.cv *= 0.98

        if(self.cv>1.0):
            self.cv = 1.0
            self.charged = True
            self.floor.create_object(AttackInfo( p=[ self.p[0], self.p[1] ], message="~charged~"))

            for s in self.cable_segments:
                self.floor.simple_tick_manager.tickables.remove(s)
                s.flash_color = [ 1.0,1.0,1.0,1.0 ]

        return True

