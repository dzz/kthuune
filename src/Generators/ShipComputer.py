from Beagle import API as BGL

class MenuTerminal:
    def setup_options(self):
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
        self.setup_options()
        self.synch_secondary_items()

    def synch_secondary_items(self):
        self.second_level_items = self.second_level_items_map[self.top_level_items[self.top_level_item]]

    def render(self):
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

    def key_up(self):
        self.second_level_item = (self.second_level_item-1) % len(self.second_level_items)

    def key_down(self):
        self.second_level_item = (self.second_level_item-1) % len(self.second_level_items)

    def key_left(self):
        self.second_level_item = 0
        self.top_level_item = (self.top_level_item-1) % len(self.top_level_items)
        self.synch_secondary_items()

    def key_right(self):
        self.second_level_item = 0
        self.top_level_item = (self.top_level_item+1) % len(self.top_level_items)
        self.synch_secondary_items()

    def key_select(self):
        print("CHOICE")

    def key_back(self):
        print("BACK")

class ShipComputer(MenuTerminal):
    pass

class TeleportControl(MenuTerminal):
    def setup_options(self):
        self.top_level_items = [ "link point" ]
        self.second_level_items_map = {
            "link point" : [
                "alpha i."
            ],
        }

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
