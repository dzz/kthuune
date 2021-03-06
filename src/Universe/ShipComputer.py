from Beagle import API as BGL
from ..KSounds import KSounds
from ..Abilities import Abilities
from Newfoundland.Object import Object
import textwrap

class TransporterFlash(Object):
    textures = BGL.assets.get("KT-player/animation/transporter_flash")

    def customize(self):
        self.buftarget = "popup"
        self.light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER
        self.tick_type = Object.TickTypes.PURGING
        self.light_radius = 20
        self.light_color = [ 1.0,0.0,1.0,1.0 ]
        self.flash_color = [ 0.9,0.8,1.0,1.0 ]
        self.texture = TransporterFlash.textures[0]
        self.anim_frame = 0
        self.size = [3.5,3.5]
        self.z_index = 9000

    def tick(self):
        if(self.anim_frame< len(TransporterFlash.textures)):
            self.texture = TransporterFlash.textures[ int(self.anim_frame) ] 
            self.anim_frame += 0.5
            self.flash_color[3] *= 0.9
            return True
        else:
            return False

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
        if len(self.second_level_items)==0:
            return
        if(self.in_menu):
            self.second_level_item = (self.second_level_item-1) % len(self.second_level_items)
            KSounds.play(KSounds.term_updown)

    def key_down(self):
        if len(self.second_level_items)==0:
            return
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

    def get_top_level_selection(self):
        return self.top_level_items[ self.top_level_item]

    def get_second_level_selection(self):
        return self.second_level_items_map[self.get_top_level_selection()][self.second_level_item]

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

        self.selected_destination = None
        self.selecting_destination = False
        self.in_menu = True
        self.synch_secondary_items()
        self.selected_system = None

    def custom_render(self):
        if self.selecting_destination is True:
            string = "Warp Target: " + self.selected_destination
            cost = 2
            if Abilities.ThoriumAmount >= 2:
                BGL.lotext.render_text_pixels(string,8,223,[ 1.0,1.0,1.0 ])
                BGL.lotext.render_text_pixels("Confirm Warp?",90,120,[ 1.0,1.0,1.0 ])
            else:
                BGL.lotext.render_text_pixels("ERROR: INSUFFICIENT THORIUM",90,120,[ 1.0,1.0,1.0 ])
            BGL.lotext.render_text_pixels("COST: {0} Thorium".format(cost),90,129,[ 1.0,1.0,1.0 ])
            BGL.lotext.render_text_pixels("AVAILABLE: {0}".format(Abilities.ThoriumAmount),90,138,[ 1.0,1.0,1.0 ])
            return
        elif(self.top_level_item==0):
            string = "Current System: " + self.owner.floor.player.current_system
            BGL.lotext.render_text_pixels(string,8,223,[ 1.0,1.0,1.0 ])

    def key_back(self):
        if self.selecting_destination:
            self.selecting_destination = False
            self.in_menu = True
            KSounds.play( KSounds.term_back )
        else:
            pass

    def key_select(self):
        if self.get_top_level_selection() == "navigation":
            if self.get_second_level_selection() == self.owner.floor.player.current_system:
                return
            if not self.selecting_destination:
                self.selected_destination = self.get_second_level_selection()
                self.selecting_destination = True
                self.in_menu = False
                KSounds.play( KSounds.term_select )
            else:
                cost = 2
                if Abilities.ThoriumAmount >= 2:
                    Abilities.ThoriumAmount -= 2
                    self.owner.floor.player.current_system = self.selected_destination 
                    self.owner.floor.game.trigger_cinematic("warp")
                pass
        else:
            pass


        
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
    

    def get_dest(self):
            player = self.owner.floor.player
            dest = player.world_map.systems[ player.current_system ]["destinations"][self.selected_destination]
            return dest

    def key_select(self):
        if(self.in_menu):
            self.in_menu = False
            self.selected_destination = self.second_level_items_map["destination"][self.second_level_item]
            KSounds.play( KSounds.term_select )
        else:
            player = self.owner.floor.player
            #dest = player.world_map.systems[ player.current_system ]["destinations"][self.selected_destination]
            dest = self.get_dest()

            def animation_finished():
                player.visible = True
                player.game.next_area( dest["area_name"], None )

            player.floor.camera.grab_cinematic(self.owner, 36, animation_finished )
            player.floor.create_object(TransporterFlash( p= [ player.p[0], player.p[1]]))
            player.visible = False

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

class CommenceBirth(TeleportControl):
    def setup_options(self):
        self.top_level_items = [ "destination" ]

        self.second_level_items_map = {
            "destination" : [ "COMMENCE BIRTH" ]
        }

        self.in_menu = True
        self.synch_secondary_items()
        self.selected_destination = None

    def get_dest(self):
        return { "unlocked" : True, "area_name" : "lacuna_canal", "pin_name" : None }

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

##########################################

class ElderMessage(MenuTerminal):

    #messages = [ "README.txt" ]
    #message_content = { "README.txt" : "ASDFASDFASDF" }

    messages = [ ]
    message_content = { }
    binaries = []
    binary_callbacks = { }

    icon_view = BGL.assets.get("KT-player/coordsys/terminal_view") 
    def setup_options(self):
        self.top_level_items = [ ]
        self.second_level_items_map = { }

        if len(ElderMessage.messages)>0:
            self.top_level_items.append("INBOX.bin")
            self.second_level_items_map["INBOX.bin"] = ElderMessage.messages
        if len(ElderMessage.binaries)>0:
            self.top_level_items.append("/usr/bin/")
            self.second_level_items_map["/usr/bin/"] = ElderMessage.binaries

        self.in_menu = True
        self.synch_secondary_items()
        self.selected_destination = None
        self.message = None
        self.inbox = False
        self.bins = False
        self.t = 0

    icon_shader = BGL.assets.get("beagle-2d/shader/beagle-2d")

    def custom_render(self):

        if not self.in_menu:
            if self.message:
                char = min(self.t // 2, len(self.message))
                x = max(1.0,float(self.t) / (len(self.message)*4))

                light_message = textwrap.wrap(self.message[0:char], 25 )

                for i,msg in enumerate(light_message):
                    BGL.lotext.render_text_pixels(msg,15,24+(i*9),[ x,x,x ])

            BGL.primitive.unit_uv_square.render_shaded(ElderMessage.icon_shader,{
                "texBuffer" : BGL.assets.get("KT-forest/texture/LORD-127"),
                "translation_local" : [ 0.0,0.0],
                "scale_local" : [ 3.8,3.8 ],
                "translation_world" : [ 10.0, -3.2 ],
                "scale_world" : [ 1.0, 1.0 ],
                "filter_color" : [ 1.0,1.0,1.0,1.0 ],
                "rotation_local" : 0.0,
                "view" : ElderMessage.icon_view
            })


    def key_select(self):
        self.reset_tick()
        KSounds.play( KSounds.term_select )

        if self.in_menu:
            self.inbox, self.bins = False, False
            if self.get_top_level_selection() == "INBOX.bin": self.inbox = True
            if self.get_top_level_selection() == "/usr/bin/": self.bins = True
            if self.inbox:
                self.in_menu = False
                self.message = ElderMessage.message_content[ self.get_second_level_selection() ]
            if self.bins:
                ElderMessage.binary_callbacks[ self.get_second_level_selection() ](self.owner)


    def key_back(self):
        if not (self.in_menu):
            self.in_menu = True
            KSounds.play( KSounds.term_back )

    def tick(self):
        if not self.in_menu:
            self.t = self.t + 1
            if(self.t <= len(self.message)*2):
                self.t = self.t + 1
            pass

    def reset_tick(self):
        self.t = 0
        pass

