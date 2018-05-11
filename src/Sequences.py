from Beagle import API as BGL
from glob import glob
from os.path import basename, splitext

from .DungeonFloor import DungeonFloor
from .Universe.AreaLoader import get_area_data
from .Abilities import Abilities
from .Universe.NPC.Elder import Elder
from .CloudBackground import CloudBackground
import audio

class Sequences:
    active_music_key = None
    titles = {
        #hard to jump in and test
        "1" : { "title" : "First, we cut...", "time_limit": 120, "music" : "KT-player/path/ship_music" },
        "2" : { "title" : "...Then, we cut some more.", "time_limit" : 40, "music" : "KT-player/path/gameplay1" },
        "3" : { "title" : "Runner's High", "time_limit" : 160, "music" : "KT-player/path/ship_music", }, #mat didn't see dash tutor
        "3.1" : { "title" : "Boppin'", "time_limit" : 70, "music" : "KT-player/path/gameplay1", }, 
        "4" : { "title" : "Kinetic Energy", "time_limit" : 120, "music" : "KT-player/path/ship_music" },
        "5" : { "title" : "Feathers in the wind", "time_limit" : 70, "music" : "KT-player/path/gameplay1" },
        "6" : { "title" : "Telephone Pole", "time_limit" : 90 , "music" : "KT-player/path/gameplay1" },
        "7" : { "title" : "Not what they seem...", "time_limit" : 120 , "music" : "KT-player/path/ship_music" },
        "8" : { "title" : "Faraday Cage", "time_limit" : 80, "music" : "KT-player/path/gameplay1" },
        "9" : { "title" : "Clerical Error", "time_limit" : 120, "music" : "KT-player/path/gameplay1" }, #debug state here, or make failure more quick & reinforcing
        "A0" :{ "title" :  "Pontiff Predicament", "time_limit" : 115, "music" : "KT-player/path/ship_music" },
    }
    found = []
    current_index = 0

    def initialize(filesystem = False):
        if filesystem:
            sequences = glob("{0}*.area".format(BGL.assets.get('KT-player/path/sequence')))
            for s in sequences:
                Sequences.found.append(splitext(basename(s))[0])
        else:
            for key in Sequences.titles:
                sequences = glob("{0}{1}.area".format(BGL.assets.get('KT-player/path/sequence'),key))
                if(len(sequences)>0):
                    Sequences.found.append(key)
                else:
                    Sequences.found.append(None)
                    #print("missing level...{0}".format(key))
                    #exit(0)

    def next(advance):
        if not advance:
            return Sequences.found[Sequences.current_index]
        idx = (Sequences.current_index+1)%len(Sequences.found)
        return Sequences.found[idx]

    def build_sequence(Game, sequence):
        Sequences.current_index = Sequences.found.index(sequence)
        afile = "{0}{1}.area".format( BGL.assets.get('KT-player/path/sequence'), sequence )
        f = open( afile, 'r')
        data = f.read()
        f.close()

        area_def = get_area_data(data)

        buildername = "{0}_{1}".format("buildarea",sequence)

        if buildername in dir(Sequences):
            return getattr(Sequences,buildername)(Game,area_def,sequence)
        else:
             return Sequences.buildarea_default(Game,area_def,sequence)



    def buildarea_default(Game,area_def, sequence):

        music = None
        if sequence in Sequences.titles:
            title = Sequences.titles[sequence]['title']
            time_limit = Sequences.titles[sequence]['time_limit']*60
            music = Sequences.titles[sequence]['music']
        else:
            title = "SEQUENCE-{0}".format(sequence)
            time_limit = 60*120


        floor = DungeonFloor( 
            time_limit = time_limit,
            music = music,
            title = title,
            god_shader = BGL.assets.get("KT-compositor/shader/sequence_god"),
            fuzz_amt = 0.8,
            fog_level_base=0.5, 
            tilescale =2, 
            uses_vision=True, 
            fade_vision_amt=0.62, 
            width = area_def["width"]*2, 
            height = area_def["height"]*2, 
            camera = Game.camera, 
            player = Game.player, 
            objects = [], 
            area_def = area_def, 
            vision_mute = 0.7,
            renderer_config = { 
                "vision_lightmap_width" : 960,
                "vision_lightmap_height" : 540,
                "photon_map_width" : 1024,
                "photon_map_height" : 1024,
                "static_lightmap_width" : 1024,
                "static_lightmap_height" : 1024,
                "dynamic_lightmap_width" : 960,
                "dynamic_lightmap_height" : 540,
                "photon_mapper_config" : {
                    'stream' : True,
                    'photon_radius' :70.0,
                    'photon_emitter_power' : 0.01,
                    'photon_decay' : 0.9,
                    'photon_decay_jitter' : 0.4,
                    'photon_max_bounces' : 9,
                    'num_photons' : 8,
                    'photon_observe_chance' : 0.8
                },
                }
            )

        floor.game = Game
        return floor

    def buildarea_1(Game,area_def,sequence):
        Elder.script = [
            "VECTORLORD!",
            "You are needed...",
            "find your sword.",
        ]
        Elder.floor_script = [
            "(elderbeast)"
        ]
        floor = Sequences.buildarea_default( Game, area_def, sequence )
        Abilities.Sword = False
        Abilities.Telekine = False
        Abilities.Dash = False
        floor.custom_background = CloudBackground()
        return floor

    def buildarea_3(Game,area_def,sequence):
        floor = Sequences.buildarea_default( Game, area_def, sequence )
        Abilities.Dash = True
        floor.custom_background = CloudBackground()
        return floor

    def buildarea_4(Game,area_def,sequence):
        Elder.texture = BGL.assets.get('KT-player/texture/elder_ii')
        Elder.script = [
            "VECTORLORD,",
            "you are not yet at full strength...",
            "the contagion is spreading, you will need to use TELEKINE powers.",
            "BEND TIME to reach WARP TOTEMS and inflict damage on ENEMIES!",
        ]
        Elder.floor_script = [
            "(elderbeast)",
            "(X) = TELEKINE"
        ]
        floor = Sequences.buildarea_default( Game, area_def, sequence )
        Abilities.Telekine = True
        floor.custom_background = CloudBackground()
        return floor

    def buildarea_7(Game,area_def,sequence):
        Elder.script = [
            "An ancient virus...",
            "...casting a field of resurrection!"
        ]
        Elder.floor_script = [
            "(elderbeast)",
            "purify OWLS to stop respawns!"
        ]
        floor = Sequences.buildarea_default( Game, area_def, sequence )
        floor.custom_background = CloudBackground()
        return floor

    def buildarea_9(Game,area_def,sequence):
        Elder.script = [
            "Devotees of corruption,",
            "...they must be taken down in groups!"
        ]
        Elder.floor_script = [
            "(elderbeast)",
            "CLERICS unlock TOTEMS"
        ]
        floor = Sequences.buildarea_default( Game, area_def, sequence )
        floor.custom_background = CloudBackground()
        return floor

    def buildarea_A0(Game,area_def,sequence):
        Elder.script = [
            "priests, they spread the word,",
            "ushering in decay.",
            "use a shield to get in close."
        ]
        Elder.floor_script = [
            "(elderbeast)",
            "watch for SHIELD TOTEMS!",
        ]
        floor = Sequences.buildarea_default( Game, area_def, sequence )
        return floor


         
