from Beagle import API as BGL
from .EditorElements.Brushes import Brushes
from .EditorElements.Brush import Brush
from glob import glob
from os.path import basename
from copy import copy
from random import choice

class LevelGenerator():

    world_size = 2
    brush_map = { 7: [], 14: []} 

    def map_brushfiles():
        paths = glob( BGL.environment.settings['app_dir'] + "/resources/brush_levels/*.brushes")
        for path in paths:
            brushfile = basename(path).split(".brushes")[0]
            Brushes.set_name(brushfile)
            Brushes.brushes = []
            Brushes.load()
            LevelGenerator.brush_map [ int(Brushes.w_size) ].append(list(Brushes.brushes))

        print(LevelGenerator.brush_map)

    def get_modded_room_brushes( x, y, size ):
        brushes = []
        room = choice(LevelGenerator.brush_map[size])
        for brush in room:
            nbrush = copy(brush)
            nbrush.x1 += x
            nbrush.x2 += x
            nbrush.y1 += y
            nbrush.y2 += y
            brushes.append(nbrush)
        return brushes

    def get_large_room_brushes( x, y ):
        return LevelGenerator.get_modded_room_brushes( x,y, 14)

    def get_small_room_brushes( x, y ):
        return LevelGenerator.get_modded_room_brushes( x,y, 7)

    def generate():
        LevelGenerator.map_brushfiles()
        brushes = []
        world = {}
        for x in range(-LevelGenerator.world_size,LevelGenerator.world_size):
            for y in range(-LevelGenerator.world_size,LevelGenerator.world_size):
                world[(x,y)] = choice (["big","small"])

        for (x,y) in world:
            if world[(x,y)] == "big":
                # place 1 large room
                brushes.extend(LevelGenerator.get_large_room_brushes((x*28)+14,(y*28)+14))
            else:
                brushes.extend(LevelGenerator.get_small_room_brushes((x*28)+7,(y*28)+7))
                brushes.extend(LevelGenerator.get_small_room_brushes((x*28)+21,(y*28)+7))
                brushes.extend(LevelGenerator.get_small_room_brushes((x*28)+7,(y*28)+21))
                brushes.extend(LevelGenerator.get_small_room_brushes((x*28)+21,(y*28)+21))

            print(len(brushes))


        Brushes.brushes = brushes
        Brush.next_id = 1
        for brush in Brushes.brushes:
            brush.id = Brush.get_next_id()

