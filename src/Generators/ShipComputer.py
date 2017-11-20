from Beagle import API as BGL
from ..KSounds import KSounds
from ..Abilities import Abilities

        

class MenuTerminal:
    def setup_options(self):
        #dummy data
        self.top_level_items = [ "navigation", "neurophagy" ]
        self.second_level_items_map = {
            "navigation" : [
                "Prologue II.",
                "Oort Cloud"
            ],
            "neurophagy" : [
                "Status",
                "Research"
            ]
        }

    def __init__(self, owner):
        self.owner = owner
        self.top_level_item = 0
        self.second_level_item = 0
        self.in_menu = True
        #self.setup_options()
        #self.synch_secondary_items()

    def synch_secondary_items(self):
        self.second_level_items = self.second_level_items_map[self.top_level_items[self.top_level_item]]

    def render_uninstalled(self):
        BGL.lotext.render_text_pixels("SYSTEM ERROR: NO SOFTWARE",60,120,[ 1.0,1.0,1.0 ])

    def render_installing(self):
        BGL.lotext.render_text_pixels("INSTALLING... {0:.2f}%".format(self.owner.install_percent),90,120,[ 1.0,1.0,1.0 ])

    def render(self):

        if not self.owner.term_installed:
            self.render_uninstalled()
            return

        if self.owner.install_percent<100:
            self.render_installing()
            return

        if(self.in_menu):
            header = ""
            for idx,item in enumerate(self.top_level_items):
                option = item
                if idx == self.top_level_item:
                    option = "[" + item + "]"
                if idx != 0:
                    header = header + "    "
                header = header + option
            BGL.lotext.render_text_pixels(header, 20,30, [1.0,1.0,1.0,1.0])

            for idx,item in enumerate(self.second_level_items):
                option = item
                if idx == self.second_level_item:
                    option = "*" + item
                BGL.lotext.render_text_pixels(option, 20,50+(idx*10), [1.0,1.0,1.0,1.0])
        self.custom_render()

    def custom_render(self):
        pass

    def key_up(self):
        if(self.in_menu):
            self.second_level_item = (self.second_level_item-1) % len(self.second_level_items)
            KSounds.play(KSounds.term_updown)

    def key_down(self):
        if(self.in_menu):
            self.second_level_item = (self.second_level_item+1) % len(self.second_level_items)
            KSounds.play(KSounds.term_updown)

    def key_left(self):
        if(self.in_menu):
            self.second_level_item = 0
            self.top_level_item = (self.top_level_item-1) % len(self.top_level_items)
            self.synch_secondary_items()
            KSounds.play(KSounds.term_leftright)

    def key_right(self):
        if(self.in_menu):
            self.second_level_item = 0
            self.top_level_item = (self.top_level_item+1) % len(self.top_level_items)
            self.synch_secondary_items()
            KSounds.play(KSounds.term_leftright)

    def key_select(self):
        pass

    def key_back(self):
        pass

class ShipComputer(MenuTerminal):
    def setup_options(self):
        self.top_level_items = [ "navigation", "neurophagy" ]
        self.second_level_items_map = {
            "navigation" : self.owner.floor.player.world_map.get_available_systems(),
            "neurophagy" : [
                "Status",
                "Research"
            ]
        }
        self.synch_secondary_items()

    def custom_render(self):
        if(self.top_level_item==0):
            string = "Current System: " + self.owner.floor.player.current_system
            BGL.lotext.render_text_pixels(string,8,223,[ 1.0,1.0,1.0 ])
        
class TeleportControl(MenuTerminal):
    def setup_options(self):
        self.top_level_items = [ "destination" ]

        self.second_level_items_map = {
            "destination" : self.owner.floor.player.world_map.get_available_destinations( self.owner.floor.player.current_system )
        }

        self.in_menu = True
        self.synch_secondary_items()
        self.selected_destination = None

    def custom_render(self):
        if not (self.in_menu):
            string = "Destination: " + self.selected_destination
            BGL.lotext.render_text_pixels(string,8,223,[ 1.0,1.0,1.0 ])
            BGL.lotext.render_text_pixels("Confirm Teleport?",90,120,[ 1.0,1.0,1.0 ])
    
    def key_select(self):
        if(self.in_menu):
            self.in_menu = False
            self.selected_destination = self.second_level_items_map["destination"][self.second_level_item]
            KSounds.play( KSounds.term_select )
        else:
            player = self.owner.floor.player
            dest = player.world_map.systems[ player.current_system ]["destinations"][self.selected_destination]
            player.game.next_area( dest["area_name"], None )

    def key_back(self):
        if not (self.in_menu):
            self.in_menu = True
            KSounds.play( KSounds.term_back )

class ReturnToShip(TeleportControl):
    def setup_options(self):
        self.top_level_items = [ "destination" ]

        self.second_level_items_map = {
            "destination" : [ "The Xeoliex" ]
        }

        self.in_menu = True
        self.synch_secondary_items()
        self.selected_destination = None


class TelekineControl(MenuTerminal):
    def setup_options(self):
        self.top_level_items = [ "activate gene", "organism" ]
        self.second_level_items_map = {
            "activate gene" : [
                "Basic Telekine"
            ],
            "organism" : [
                "Status",
                "Feed"
            ]
        }
        self.synch_secondary_items()

class SwordControl(MenuTerminal):
    def setup_options(self):
        self.top_level_items = [ "infusion", "materials" ]
        self.second_level_items_map = {
            "infusion" : [
                "slash tech"
            ],
            "materials" : [
                "process"
            ]
        }
        self.synch_secondary_items()

