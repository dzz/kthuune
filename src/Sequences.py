from Beagle import API as BGL
from glob import glob
from os.path import basename, splitext

from .DungeonFloor import DungeonFloor
from .Universe.AreaLoader import get_area_data
from .Abilities import Abilities
from .Universe.NPC.Elder import Elder

class Sequences:
    titles = {
        "1" : "First, we cut...",
        "2" : "...Then, we cut some more.",
        "3" : "Runner's High",
        "4" : "Kinetic Energy",
        "5" : "Feathers in the wind",
        "6" : "Telephone Pole",
        "7" : "",
        "8" : "",
        "9" : "",
        "A0" : "",
        "A1" : "",
        "A2" : "",
        "A3" : "",
        "A4" : "",
        "A5" : "",
        "A6" : ""
    }
    found = []
    current_index = 0

    def initialize():
        sequences = glob("{0}*.area".format(BGL.assets.get('KT-player/path/sequence')))
        for s in sequences:
            Sequences.found.append(splitext(basename(s))[0])

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

        if sequence in Sequences.titles:
            title = Sequences.titles[sequence]
        else:
            title = "SEQUENCE-{0}".format(sequence)

        floor = DungeonFloor( 
            music = BGL.assets.get("KT-player/path/ship_music"),
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
            "(an elderbeast)"
        ]
        floor = Sequences.buildarea_default( Game, area_def, sequence )
        Abilities.Sword = False
        Abilities.Telekine = False
        Abilities.Dash = False
        return floor

    def buildarea_3(Game,area_def,sequence):
        floor = Sequences.buildarea_default( Game, area_def, sequence )
        Abilities.Dash = True
        return floor

    def buildarea_4(Game,area_def,sequence):
        Elder.script = [
            "VECTORLORD,",
            "you are not yet at full strength...",
            "the contagion is spreading, you will need to use TELEKINE powers.",
            "BEND TIME to reach WARP TOTEMS and inflict damage on ENEMIES!",
        ]
        Elder.floor_script = [
            "(an elderbeast)",
            "(X) = TELEKINE"
        ]
        floor = Sequences.buildarea_default( Game, area_def, sequence )
        Abilities.Telekine = True
        return floor

         
