from Beagle import API as BGL
from glob import glob
from os.path import basename, splitext

from .DungeonFloor import DungeonFloor
from .Universe.AreaLoader import get_area_data
from .Abilities import Abilities
from .Universe.NPC.Elder import Elder
from .CloudBackground import CloudBackground
from .Universe.LevelProps.SpeechBubble import SpeechBubble
from .Universe.ShipComputer import ElderMessage
import audio


def build_bimodal_fp_trigger(vx, vy):
    def handler(trigger):
        if trigger.floor.forced_progression:
            trigger.floor.end_forced_progression()
        else:
            trigger.floor.start_forced_progression(vx,vy)
    return handler

class Sequences:
    start_level = "z"
    active_music_key = None
    titles = {
        "0" : { "title" : "Debug Area", "time_limit": 999, "music" : "KT-player/path/ship_music" },
        "0.1" : { "title" : "RootKit 1.0", "time_limit": 999, "music" : "KT-player/path/ship_music" },

        "1" : { "title" : "First, Cut!", "time_limit": 40, "music" : "KT-player/path/ship_music" },
        "2" : { "title" : "Kindergarten", "time_limit" : 35, "music" : "KT-player/path/polydrone" },
        "3" : { "title" : "Runner's High", "time_limit" : 30, "music" : "KT-player/path/polydrone", }, #mat didn't see dash tutor
        "3.1" : { "title" : "Boppin'", "time_limit" : 30, "music" : "KT-player/path/trixymixy", }, 
        "4" : { "title" : "Kinetic Energy", "time_limit" : 30, "music" : "KT-player/path/trixymixy" },
        "4.1" : { "title" : "Oxytoxicity", "time_limit" : 30, "music" : "KT-player/path/trixymixy" },
        "5" : { "title" : "Feathers in the wind", "time_limit" : 25, "music" : "KT-player/path/lacuna_canal" },
        "6" : { "title" : "Telephone Pole", "time_limit" : 25 , "music" : "KT-player/path/polydrone" },
        "7" : { "title" : "Not what they seem...", "time_limit" : 45 , "music" : "KT-player/path/polydrone" }, # can fuck yourself up
        "8" : { "title" : "Faraday Cage", "time_limit" : 25, "music" : "KT-player/path/trixymixy" },
        "9" : { "title" : "Clerical Error", "time_limit" : 35, "music" : "KT-player/path/trixymixy" }, #debug state here, or make failure more quick & reinforcing
        "tt" : { "title" : "Instant Cooking", "time_limit" : 15, "music" : "KT-player/path/trixymixy" }, #debug state here, or make failure more quick & reinforcing
        "A0" :{ "title" :  "Pontiff Predicament", "time_limit" : 45, "music" : "KT-player/path/trixymixy" },
        "A1" :{ "title" :  "Slapped on the Wrist", "time_limit" : 40, "music" : "KT-player/path/trixymixy" },
        "z" :{ "title" :  "fptest", "time_limit" : 40, "music" : "KT-player/path/trixymixy" },
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
                    print("missing level...{0}".format(key))
                    exit(0)

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
        buildername = "{0}_{1}".format("buildarea",sequence.replace('.','_'))
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
            if "slash_limit" in Sequences.titles[sequence]:
                slash_limit = Sequences.titles[sequence]['slash_limit']
            else:
                slash_limit = 10
        else:
            title = "SEQUENCE-{0}".format(sequence)
            time_limit = 60*120


        floor = DungeonFloor( 
            slash_limit = slash_limit,
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

    def buildarea_0(Game,area_def,sequence):
        floor = Sequences.buildarea_default( Game, area_def, sequence )
        Abilities.Sword = True
        Abilities.Telekine = True
        Abilities.Dash = True
        #floor.custom_background = CloudBackground()
        floor.parallax_skin = "ks"
        floor.genocide_enabled = False

        def test_trigger(owner):
            SpeechBubble.spawn(owner, [ "LEFT STICK to Move"] )
            #bubble = SpeechBubble( triggered = True, visible = True, p = list(owner.p), mode = 1 ) 
            #owner.floor.create_object(bubble)
            #bubble.set_script( [ "LEFT STICK to Move" ], owner.p, False )
        
        floor.trigger_callbacks[0] = test_trigger
        ElderMessage.binaries = [ "continue" ]
        def bin_continue(owner):
            owner.floor.player.terminal_size = 0.0
            owner.floor.player.active_terminal = None
            owner.floor.player.tick()
            owner.floor.player.game.next_sequence()

        ElderMessage.binary_callbacks["continue"] = bin_continue
        return floor

    def buildarea_0_1(Game,area_def,sequence):
        floor = Sequences.buildarea_default( Game, area_def, sequence )
        Abilities.Sword = False
        Abilities.Telekine = False
        Abilities.Dash = True
        #floor.custom_background = CloudBackground()
        floor.parallax_skin = "ks"
        floor.genocide_enabled = False

        def move_trigger(owner):
            SpeechBubble.spawn(owner, [ "LEFT STICK to Move"] )

        def look_trigger(owner):
            SpeechBubble.spawn(owner, [ "RIGHT STICK to Look"] )

        def run_trigger(owner):
            SpeechBubble.spawn(owner, [ "RB to Sprint"] )

        def gj_trigger(owner):
            SpeechBubble.spawn(owner, [ "...", "good!"] )

        def dash_trigger(owner):
            SpeechBubble.spawn(owner, [ "B to Tele-Dash"] )
        
        floor.trigger_callbacks[0] = move_trigger
        floor.trigger_callbacks[1] = look_trigger
        floor.trigger_callbacks[2] = run_trigger
        floor.trigger_callbacks[3] = gj_trigger
        floor.trigger_callbacks[4] = dash_trigger

        Elder.script = [ 
            "VECTORLORD...",
            "I am a greybeard.",
            "...",
            "You are one of our Subprocesses, and if you do not succeed..."
            "...our Systems will fail."
        ]
        Elder.floor_script = [] 

        ElderMessage.messages = [ "README.nfo", "skeline.txt", "worm.txt" ]
        ElderMessage.message_content = { "README.nfo" : 
        "Thank you for purchasing VECTORLORD, the world's first artificially intelligent antivirus for business class QPUs! We're certain your corporation will be satisfied with it's performance. Our SLA ensures bad sectors will be purified within guaranteed time-limits. If the AI Agent fails, its will be permanently terminated!\n\n Have a happy Tuesday!",
            "skeline.txt" : "Us at RUSKER have identified the Skeline as the primary infectant that targets Q-Processes. Typically seen in packs, they can be a nuisance when they get into the crevices of a sector.",
            "worm.txt" : "Worms are an annoyance, but not technically quantum and therefore ignored by purification checks." } 

        ElderMessage.binaries = [ "continue" ]
        def bin_continue(owner):
            owner.floor.player.terminal_size = 0.0
            owner.floor.player.active_terminal = None
            owner.floor.player.tick()
            owner.floor.player.game.trigger_cinematic("warp")
            owner.floor.player.game.next_sequence()

        ElderMessage.binary_callbacks["continue"] = bin_continue

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
        Abilities.Dash = True
        floor.custom_background = CloudBackground()
        return floor

    def buildarea_3(Game,area_def,sequence):
        Abilities.Dash = True
        Elder.script = [ "VECTORLORD, you must move quickly!",
                         "RUN with [RB] or DASH with (B)",
                         "combine techniques for precision movement" ]
        Elder.floor_script = [
            "[RB] to RUN (B) to DASH"
        ]
        floor = Sequences.buildarea_default( Game, area_def, sequence )
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

    def buildarea_4_1(Game,area_def,sequence):
        Elder.texture = BGL.assets.get('KT-player/texture/elder0000')
        Elder.script = [ "...strange mutations in the source these days...",
                         "the key, perhaps, to reproduction!" ]
        Elder.floor_script = [ "(elderbeast)" ]
        floor = Sequences.buildarea_default( Game, area_def, sequence )
        return floor

    def buildarea_7(Game,area_def,sequence):
        Elder.texture = BGL.assets.get('KT-player/texture/elder_iii')
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

    def buildarea_z(Game,area_def,sequence):
        floor = Sequences.buildarea_default( Game, area_def, sequence )
        floor.trigger_callbacks[0] = build_bimodal_fp_trigger(0.3,0.0)
        return floor

         
