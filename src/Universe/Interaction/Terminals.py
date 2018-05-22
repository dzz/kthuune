from Newfoundland.Object import Object
from Beagle import API as BGL
from ..ShipComputer import *
from ...Abilities import Abilities
from ..LevelProps.Telekine import Telekine
from random import choice

class FTerm(Object):
    def parse(od,df):
        ret = []

        title = "Commence Birth"
        if "title" in od["meta"]: title=od["meta"]["title"]

        ret.append(FTerm(p=[od["x"],od["y"]]))
        ret.append(FTermStand(p=[od["x"],od["y"]]))
        ret.append(Terminal(title=title, p=[od["x"],od["y"]]))
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
