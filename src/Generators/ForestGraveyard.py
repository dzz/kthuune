from random import uniform, choice
from math import hypot


def map_txt_spec( df, txt_spec, probability, effect  ):
    for row_idx,row in enumerate(txt_spec):
        row_spec = row[0].replace(" ","")
        for col_idx,char in enumerate(row_spec):
            x = (float(col_idx) / float(len(row_spec))) * float( df.width )
            y = (float(row_idx) / float(len(txt_spec))) * float( df.height )

            if(uniform(0.0,1.0) < probability ):
                effect( char,[x,y] )

class ForestGraveyard():
    def __init__(self):
        pass

    def compile(self, dungeon_floor ):
        self.generate_sigil_points( dungeon_floor )
        self.generate_tiledata(  dungeon_floor )

    def get_tiledata(self):
        return self.tile_data

    def get_sigil_tiledata( self, sigil ):

        print(sigil)
        if sigil == "#":
            return choice( range(14,20) )
        if sigil == "_":
            return choice( range(4,8) )
        if sigil == "y":
            return choice( range(4,5) )
        if sigil == "`":
            return choice( range(1,3) )
        if sigil == "X":
            return choice( range(10,14) )
        exit()

            
    def generate_tiledata( self, df ):
        print(self.sigil_points)
        tile_data = [0]*(df.width*df.height)
        for x in range(0, df.width):
            print(x)
            for y in range(0, df.height):
                print(y)
                closest_sigil_point = None
                score = None
                for sigil_point in self.sigil_points:
                    d = hypot( sigil_point["p"][0]-x, sigil_point["p"][1]-y)
                    if not score:
                        score = d
                        closest_sigil_point = sigil_point
                    elif d < score:
                        closest_sigil_point = sigil_point
                        score = d
                print(closest_sigil_point["sigil"])
                tile_data[  (y * df.width) + x ]  = self.get_sigil_tiledata(closest_sigil_point["sigil"])

        self.tile_data = tile_data

    def generate_trees( self, df ):
        pass



    def generate_sigil_points( self, df):
        txt_spec = [
            [ "# # # # # # # # # #" ],
            [ "# _ _`_ _ _ ` _ _ #" ],
            [ "#_ XX` yyyy_`_XX _#" ],
            [ "#_ XX` yyyy_`_XX _#" ],
            [ "#_ _ ` ` ` ``_ _ _#" ],
            [ "#_ XX_ _ _ _ _XX _#" ],
            [ "#_ XX_ _ ` _ _XX _#" ],
            [ "#_ _ _ _ ` _ ___ _#" ],
            [ "#_ XX_ _ ` _ _XX _#" ],
            [ "#_ XX_ _ ` _ _XX _#" ],
            [ "#_ _ _ _ ` _ _ _ _#" ],
            [ "# # # # # # # # # #" ] ]

        sigil_points = []

        map_txt_spec( df, txt_spec, 0.8, lambda char, p : sigil_points.append({ "sigil": char, "p": p } ) )
        self.sigil_points = sigil_points

