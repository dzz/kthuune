from Beagle import API as BGL
from glob import glob
from os.path import basename, splitext

from .DungeonFloor import DungeonFloor
from .Universe.AreaLoader import get_area_data

class Sequences:
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
            return getattr(Seqences,buildername)(Game,area_def,sequence)
        else:
             return Sequences.buildarea_default(Game,area_def,sequence)


    def buildarea_default(Game,area_def, sequence):
        floor = DungeonFloor( 
            music = BGL.assets.get("KT-player/path/ship_music"),
            title = "SEQUENCE-{0}".format(sequence),
            god_shader = BGL.assets.get("KT-compositor/shader/ship_god"),
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

         
