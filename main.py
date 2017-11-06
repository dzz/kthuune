from .src.Game import Game

class glb:
    tick = 0
    game = Game()
    ini = None

def init():
    glb.game.init()

def tick():
    glb.tick+=1
    if(glb.tick>630):
        glb.tick = 0
        del glb.game
        glb.game = Game()
        glb.game.configure( glb.ini )
    else:
        glb.game.tick()

def render():
    glb.game.render()

def finalize():
    glb.game.finalize()

def configure( application_ini ):
    glb.ini = application_ini
    glb.game.configure( application_ini )
