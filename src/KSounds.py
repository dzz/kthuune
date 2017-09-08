import audio
from Beagle import API as BGL

class KSounds:
    charge_initiated = audio.baudy_load_sound(BGL.assets.get("KT-player/path/charge_initiated")) 
    charge_executed = audio.baudy_load_sound(BGL.assets.get("KT-player/path/charge_executed")) 
    snap_landed = audio.baudy_load_sound(BGL.assets.get("KT-player/path/snap_landed")) 
    basic_hit = audio.baudy_load_sound(BGL.assets.get("KT-player/path/basic_hit")) 
    crit = audio.baudy_load_sound(BGL.assets.get("KT-player/path/crit")) 
    enemy_killed = audio.baudy_load_sound(BGL.assets.get("KT-player/path/enemy_killed")) 
    player_hurt = audio.baudy_load_sound(BGL.assets.get("KT-player/path/player_hurt")) 
    enemy_projectile = audio.baudy_load_sound(BGL.assets.get("KT-player/path/enemy_projectile")) 
    #combo = audio.baudy_load_sound(BGL.assets.get("KT-player/path/combo")) 

    def play(sound_id):
        audio.baudy_play_sound(sound_id)
