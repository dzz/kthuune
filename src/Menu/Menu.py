from Beagle import API as BGL
from ..KSounds import KSounds
import audio

def start_game():
    Menu.Game.main_menu = False
    #audio.baudy_play_music( BGL.assets.get("KT-player/path/gameplay1"))
    Menu.initialized = False

def quit_game():
    exit()

class Menu:
    initialized = False
    texture_title = BGL.assets.get("KT-player/texture/menu_title")
    primitive = BGL.primitive.unit_uv_square
    shader = BGL.assets.get("KT-player/shader/menu_base")
    t = 0.0
    texbuffer = BGL.framebuffer.from_dims( 480, 270 )

    UP_STATE = [ False, False ]
    UP_PRESSED = False
    DOWN_STATE = [ False, False ]
    DOWN_PRESSED = False
    A_PRESSED = False
    A_STATE = [ False, False ]

    current_options = [
        { "label" : "Start New Game", "callback" : start_game },
        { "label" : "The Story So Far" },
        { "label" : "How To Play" },
        { "label" : "Settings" },
        { "label" : "Credits" },
        { "label" : "Quit", "callback" : quit_game },
    ]

    current_selection = 0

    def tick():
        Menu.controllers.tick()
        pad = Menu.controllers.get_virtualized_pad(0)
        Menu.A_STATE[0] = Menu.A_STATE[1]
        Menu.A_STATE[1] = pad.button_down( BGL.gamepads.buttons.A )
        if Menu.A_STATE[1] is True and Menu.A_STATE[0] is False:
            Menu.A_PRESSED = True
        else:
            Menu.A_PRESSED = False
        Menu.UP_STATE[0] = Menu.UP_STATE[1]
        Menu.UP_STATE[1] = pad.button_down( BGL.gamepads.buttons.DPAD_UP )
    
        if Menu.UP_STATE[1] is True and Menu.UP_STATE[0] is False:
            Menu.UP_PRESSED = True
        else:
            Menu.UP_PRESSED = False

        Menu.DOWN_STATE[0] = Menu.DOWN_STATE[1]
        Menu.DOWN_STATE[1] = pad.button_down( BGL.gamepads.buttons.DPAD_DOWN )
    
        if Menu.DOWN_STATE[1] is True and Menu.DOWN_STATE[0] is False:
            Menu.DOWN_PRESSED = True
        else:
            Menu.DOWN_PRESSED = False
        Menu.t += 0.003;
        if(Menu.t>1000):
            Menu.t = 0

        if(Menu.DOWN_PRESSED):
            Menu.current_selection  = (Menu.current_selection+1)%len(Menu.current_options)
            KSounds.play(KSounds.term_updown)
        if(Menu.UP_PRESSED):
            Menu.current_selection  = (Menu.current_selection-1)%len(Menu.current_options)
            KSounds.play(KSounds.term_updown)
        if(Menu.A_PRESSED):
            opt = Menu.current_options[Menu.current_selection]
            if "callback" in opt: 
                opt["callback"]()
    
    def render():

        if not Menu.initialized:
            #audio.baudy_play_music( BGL.assets.get("KT-player/path/vectormenu"))
            Menu.initialized = True
            
        with BGL.context.render_target( Menu.texbuffer ):

            BGL.context.clear(  0.0,0.0,0.0,0.0 )
            with BGL.blendmode.alpha_over:

                for i,option in enumerate(Menu.current_options):
                    os = "   "
                    cs = "   "
                    color = [ 0.5, 0.5, 0.5 ]
                    if(i == Menu.current_selection):
                        os = " ~*["
                        cs = "]*~ "
                        color = [ 1.0,1.0,1.0 ]

                    comp = os + option["label"] + cs
                    l = len(comp)
                    x = (480/2)-(l*4)
                    BGL.lotext.render_text_pixels(comp, x,1+(120+(11*i)), [0.0,0.0,0.0] )
                    BGL.lotext.render_text_pixels(comp, x,120+(11*i), color )


        with BGL.blendmode.alpha_over:
            Menu.primitive.render_shaded( Menu.shader, {
                "texBuffer" : Menu.texture_title,
                "tick" : Menu.t
            })
            Menu.texbuffer.render_processed(BGL.assets.get("beagle-2d/shader/passthru"))

