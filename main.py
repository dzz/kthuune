import cProfile
import beagle_runtime

pr = cProfile.Profile()

class glb:
    tick = 0
    ini = None
    editor = False

def init():
    #pr.enable()
    glb.game.init()

def tick():
    glb.game.tick()

def render():
    glb.game.render()

def finalize():
    #pr.disable()
    #pr.print_stats()
    glb.game.finalize()

def dispatch_mousedown(button,x,y):
    if glb.editor:
        glb.game.dispatch_mousedown(button,x,y)

def dispatch_mouseup(button,x,y):
    if glb.editor:
        glb.game.dispatch_mouseup(button,x,y)

def dispatch_mousemotion(x,y):
    if glb.editor:
        glb.game.dispatch_mousemotion(x,y)

def dispatch_mousewheel(y):
    if glb.editor:
        glb.game.dispatch_mousewheel(y)

def configure( application_ini ):
    glb.ini = application_ini

    if( beagle_runtime.get_user_specified_config_string() == "edit"):
        from .src.Editor import Editor
        glb.editor = True
        glb.game = Editor()
        glb.game.__shell__ = globals()["__shell__"]
    else:
        from .src.Game import Game
        glb.game = Game()
    
    glb.game.configure( application_ini )
