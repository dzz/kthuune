import audio
from Beagle import API as BGL
from random import choice

class KSounds:
    charge_initiated = audio.baudy_load_sound(BGL.assets.get("KT-player/path/charge_initiated")) 
    charge_executed = audio.baudy_load_sound(BGL.assets.get("KT-player/path/charge_executed")) 
    snap_landed = audio.baudy_load_sound(BGL.assets.get("KT-player/path/snap_landed")) 
    basic_hit = audio.baudy_load_sound(BGL.assets.get("KT-player/path/basic_hit")) 
    crit = audio.baudy_load_sound(BGL.assets.get("KT-player/path/crit")) 
    enemy_killed = audio.baudy_load_sound(BGL.assets.get("KT-player/path/enemy_killed")) 
    enemy_killed2 = audio.baudy_load_sound(BGL.assets.get("KT-player/path/enemy_killed2")) 
    player_hurt = audio.baudy_load_sound(BGL.assets.get("KT-player/path/player_hurt")) 
    enemy_projectile = audio.baudy_load_sound(BGL.assets.get("KT-player/path/enemy_projectile")) 
    enemy_projectile2 = audio.baudy_load_sound(BGL.assets.get("KT-player/path/enemy_projectile2")) 
    health = audio.baudy_load_sound(BGL.assets.get("KT-player/path/health")) 
    pickup = audio.baudy_load_sound(BGL.assets.get("KT-player/path/pickup")) 
    dash = audio.baudy_load_sound(BGL.assets.get("KT-player/path/dash")) 
    charging_projectile = audio.baudy_load_sound(BGL.assets.get("KT-player/path/charging_projectile")) 
    taking_off = audio.baudy_load_sound(BGL.assets.get("KT-player/path/taking_off")) 
    taking_off2 = audio.baudy_load_sound(BGL.assets.get("KT-player/path/taking_off2")) 
    lifting_off = audio.baudy_load_sound(BGL.assets.get("KT-player/path/lifting_off")) 
    acolyte_hustle = audio.baudy_load_sound(BGL.assets.get("KT-player/path/acolyte_hustle")) 
    totem_hit = audio.baudy_load_sound(BGL.assets.get("KT-player/path/totem_hit")) 
    totem_restored = audio.baudy_load_sound(BGL.assets.get("KT-player/path/totem_restored")) 
    groovy = audio.baudy_load_sound(BGL.assets.get("KT-player/path/groovy")) 
    tubular = audio.baudy_load_sound(BGL.assets.get("KT-player/path/tubular")) 
    walk1 = audio.baudy_load_sound(BGL.assets.get("KT-player/path/walk1")) 
    walk2 = audio.baudy_load_sound(BGL.assets.get("KT-player/path/walk2")) 
    rain_20sec = audio.baudy_load_sound(BGL.assets.get("KT-player/path/rain_20sec")) 
    rain_21sec = audio.baudy_load_sound(BGL.assets.get("KT-player/path/rain_21sec")) 
    cleric_charge = audio.baudy_load_sound(BGL.assets.get("KT-player/path/cleric_charge")) 
    cleric_triggered = audio.baudy_load_sound(BGL.assets.get("KT-player/path/cleric_triggered")) 
    slash = audio.baudy_load_sound(BGL.assets.get("KT-player/path/slash")) 
    slashhit = audio.baudy_load_sound(BGL.assets.get("KT-player/path/slashhit")) 
    redirect = audio.baudy_load_sound(BGL.assets.get("KT-player/path/redirect")) 
    terminal_open = audio.baudy_load_sound(BGL.assets.get("KT-player/path/terminal_open")) 
    terminal_close = audio.baudy_load_sound(BGL.assets.get("KT-player/path/terminal_close")) 
    term_leftright = audio.baudy_load_sound(BGL.assets.get("KT-player/path/term_leftright")) 
    term_updown = audio.baudy_load_sound(BGL.assets.get("KT-player/path/term_updown")) 
    term_select = audio.baudy_load_sound(BGL.assets.get("KT-player/path/term_select")) 
    term_back = audio.baudy_load_sound(BGL.assets.get("KT-player/path/term_back")) 

    typewriter_keys = [
        audio.baudy_load_sound(BGL.assets.get("KT-player/path/tkey1")) ,
        audio.baudy_load_sound(BGL.assets.get("KT-player/path/tkey2")) ,
        audio.baudy_load_sound(BGL.assets.get("KT-player/path/tkey3")) ,
        audio.baudy_load_sound(BGL.assets.get("KT-player/path/tkey4")) 
    ]
    typewriter_return = audio.baudy_load_sound(BGL.assets.get("KT-player/path/treturn")) 

    def play(sound_id):
        audio.baudy_play_sound(sound_id)

    def play_eproj():
        KSounds.play( choice([ KSounds.enemy_projectile, KSounds.enemy_projectile2]))
    
