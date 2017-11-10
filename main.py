import cProfile
from .src.Game import Game

pr = cProfile.Profile()

class glb:
    tick = 0
    game = Game()
    ini = None

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

def configure( application_ini ):
    glb.ini = application_ini
    glb.game.configure( application_ini )
