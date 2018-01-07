from Beagle import API as BGL
from .EditorElements.Brushes import Brushes
from .EditorElements.BrushFile import BrushFile
import glob
from random import choice
from .EditorElements.World import World

class BrushNetwork:

    collected_brushes = {}
    above = {}
    below = {}
    left = {}
    right = {}
    level_map = {}

    def parse():
        folder = BrushFile.get_folder()
        filenames = glob.glob(folder + "*.brushes")
        collected_brushes = {}

        for filename in filenames:
            BrushFile.load( Brushes, filename )
            collected_brushes[ Brushes.level_name ] = Brushes.brushes

        BrushNetwork.collected_brushes = collected_brushes
        BrushNetwork.compute_map()

    def compute_map():
        for key in BrushNetwork.collected_brushes:
            print(key)
            for brush in BrushNetwork.collected_brushes[key]:
                if brush.polyfill_key == 'generate_above':
                    if not (brush.get_link_w()) in BrushNetwork.below:
                        BrushNetwork.below[ brush.get_link_w()] = []
                    BrushNetwork.below[ brush.get_link_w() ].append(key)
                elif brush.polyfill_key == 'generate_below':
                    if not (brush.get_link_w()) in BrushNetwork.above:
                        BrushNetwork.above[ brush.get_link_w()] = []
                    BrushNetwork.above[ brush.get_link_w() ].append(key)
                elif brush.polyfill_key == 'generate_left':
                    if not (brush.get_link_h()) in BrushNetwork.right:
                        BrushNetwork.right[ brush.get_link_h()] = []
                    BrushNetwork.right[ brush.get_link_h() ].append(key)
                elif brush.polyfill_key == 'generate_right':
                    if not (brush.get_link_h()) in BrushNetwork.left:
                        BrushNetwork.left[ brush.get_link_h()] = []
                    BrushNetwork.left[ brush.get_link_h() ].append(key)

        BrushNetwork.level_map = {} 
        BrushNetwork.level_map['above'] = BrushNetwork.above
        BrushNetwork.level_map['below'] = BrushNetwork.below
        BrushNetwork.level_map['left'] = BrushNetwork.left
        BrushNetwork.level_map['right'] = BrushNetwork.right

    def move_up(key, trigger):

        above = list(filter( lambda x: x.polyfill_key == 'generate_below', Brushes.brushes))[0]
        print(above.x1, above.x2, above.y1, above.y2)

        stashed = list(Brushes.brushes)

        Brushes.set_name(key)
        Brushes.load()

        below = list(filter( lambda x: x.polyfill_key == 'generate_above', Brushes.brushes))[0]

        y_delta = above.y1 - below.y2
        x_delta = above.x1 - below.x1
        print(below.x1, below.x2, below.y1, below.y2)

        for brush in Brushes.brushes:
            brush.y1 -= y_delta
            brush.y2 -= y_delta
            brush.x1 -= x_delta
            brush.x2 -= x_delta

        for brush in stashed:
            brush.age += 1
        stashed.extend(Brushes.brushes)
        return stashed

    def move_down(key, trigger):
        Brushes.set_name(key)
        Brushes.load()

    def move_left(key, trigger):
        Brushes.set_name(key)
        Brushes.load()

    def move_right(key, trigger):
        Brushes.set_name(key)
        Brushes.load()

