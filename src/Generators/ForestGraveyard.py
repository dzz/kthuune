from random import uniform, choice
from math import hypot
from Newfoundland.Object import Object

def map_txt_spec( df, txt_spec, probability, times, jitter, effect  ):
    for row_idx,row in enumerate(txt_spec):
        row_spec = row[0]
        for col_idx,char in enumerate(row_spec):
            x = (float(col_idx) / float(len(row_spec))) * float( df.width )
            y = (float(row_idx) / float(len(txt_spec))) * float( df.height )
            if char is not ' ':
                for i in range(0,times):
                    if(uniform(0.0,1.0) < probability ):
                        effect( char,[x+uniform(-1*jitter,jitter),y+uniform(-1*jitter,jitter)] )

class ForestGraveyard():
    def __init__(self):
        pass

    def compile(self, dungeon_floor ):
        self.generate_sigil_points( dungeon_floor )
        self.generate_tiledata(  dungeon_floor )
        self.generate_trees( dungeon_floor )
        self.generate_photon_emitters(dungeon_floor)

        self.light_occluders = self.tree_occluders
        self.light_occluders.extend( self.get_base_occluders(dungeon_floor) )

        self.objects = []
        self.generate_static_lights(dungeon_floor)
        

    def get_objects(self):
        return self.objects

    def get_base_occluders(self, df):
        lines = [
            [ [-0.5*df.width, -0.5*df.height],[0.5*df.width, -0.5*df.height] ],
            [ [ 0.5*df.width, -0.5*df.height],[0.5*df.width, 0.5*df.height] ],
            [ [0.5*df.width, 0.5*df.height],[-0.5*df.width, 0.5*df.height] ],
            [ [-0.5*df.width, 0.5*df.height],[-0.5*df.width, -0.5*df.height] ]
        ]
        return lines

    def get_light_occluders(self):
        return self.light_occluders

    def get_tiledata(self):
        return self.tile_data
    
    def get_photon_emitters(self):
        return self.photon_emitters

    def get_sigil_tiledata( self, sigil ):

        print(sigil)
        if sigil == "#":
            return choice( range(1,20) )
        if sigil == "_":
            return choice( range(10,20) )
        if sigil == "y":
            return choice( range(5,15) )
        if sigil == "`":
            return choice( range(1,10) )
        if sigil == "X":
            return choice( range(2,18) )
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




    def generate_static_lights(self, df):
        static_lights = []
        txt_spec = [
            [ "  1     1  " ],
            [ " 2   3   2 " ],
            [ "  1     1  " ] 
        ]

        def generate_light(char, p):
            p[0] = p[0]-(df.width/2) + uniform(-1.0,1.0)
            p[1] = p[1]-(df.height/2) + uniform(-1.0,1.0)

            light_styles = {
                '1' : [ Object.LightTypes.STATIC_SHADOWCASTER, [ 0.1,0.3,0.1,1.0], 25.0 ],
                '2' : [ Object.LightTypes.STATIC_SHADOWCASTER, [ 0.5,0.3,0.8,1.0], 50.0 ],
                '3' : [ Object.LightTypes.STATIC_SHADOWCASTER, [ 0.8,0.6,0.0,1.0], 100.0 ],
            } 

            style = light_styles[char]

            return [ Object( visible = False, light_type = style[0], p = p, light_radius=style[2], color = list( map( lambda x: x*0.7,style[1]))) ]

        map_txt_spec( df, txt_spec, 1.0, 2, 25.0, lambda char, p : static_lights.extend(generate_light(char, p)))
        self.objects.extend( static_lights )


    def generate_photon_emitters(self, df):
        photon_emitters = []
        txt_spec = [
            [ "2,,,,,,2" ],
            [ ",2,11,2," ],
            [ ",,,11,,," ],
            [ "3,3113,3" ],
            [ ",,,11,,," ],
            [ ",2,11,2," ],
            [ "2,,,,,,2" ]
         ]

        def generate_emitter(char,p):
            if char is ',':
                return []
            p[0] = p[0]-(df.width/2) + uniform(-1.0,1.0)
            p[1] = p[1]-(df.height/2) + uniform(-1.0,1.0)

            colormap = {
                "1" : [ 0.3,0.5,0.4 ], #moonlight?
                "2" : [ 0.3,0.2,0.01 ], #sinister red?
                "3" : [ 0.5,0.61,0.3 ], #desaturated evening light?
            }
            emitter_def = [ p[0],p[1], 1.0,1.0, colormap[char] ]
            return [ emitter_def ]

        map_txt_spec( df, txt_spec, 0.6, 3, 3.0, lambda char, p : photon_emitters.extend(generate_emitter(char, p)))
        self.photon_emitters = photon_emitters

    def generate_trees( self, df ):
        txt_spec = [
            [ "Q Q Q Q Q Q Q Q Q Q" ],
            [ "Q _ _`_ _ _ ` _ _ Q" ],
            [ "Q_ ee` yyyy_`_ee _Q" ],
            [ "Q_ ee` yyyy_`_ee _Q" ],
            [ "Q_ _ ` ` ` ``_ _ _Q" ],
            [ "Q_ ee_ _ _ _ _ee _Q" ],
            [ "Q_ ee_ _ ` _ _ee _Q" ],
            [ "Q_ _ _ _ ` _ ___ _Q" ],
            [ "Q_ ee_ _ ` _ _ee _Q" ],
            [ "Q_ ee_ _ ` _ _ee _Q" ],
            [ "Q_ _ _ _ ` _ _ _ _Q" ],
            [ "Q Q Q Q Q Q Q Q Q Q" ] ]

        tree_occluders = []

        def generate_tree(char,p):
            size = None
            if char == "Q":
                size = uniform(3.5,16.2)
            if char == "e":
                size = uniform(1.3,5.6)
            if char == "`":
                size = 0.6


            if(size is None):
                return []

            p[0] = p[0]-(df.width/2) + uniform(-1.0,1.0)
            p[1] = p[1]-(df.height/2) + uniform(-1.0,1.0)
            points = []

            points.append( [ 0.0, -1*size ] )
            points.append( [ size, 0.0 ] )
            points.append( [ 0.0, 1*size ] )
            points.append( [ -1*size, 0.0 ] )

            for point in points:
                point[0] = point[0] + p[0] + uniform(-0.1 * size, 0.1*size )
                point[1] = point[1] + p[1] + uniform(-0.1 * size, 0.1*size )

            lines = []
            lines.extend( [ [ points[0], points[1] ] , [ points[1], points[2] ] , [ points[2], points[3] ] , [ points[3], points[0] ] ] )
            return lines

        map_txt_spec( df, txt_spec, 0.9, 1, 2.0, lambda char, p : tree_occluders.extend(generate_tree(char, p)))
        self.tree_occluders = tree_occluders 

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

        map_txt_spec( df, txt_spec, 0.8, 2, 1.0, lambda char, p : sigil_points.append({ "sigil": char, "p": p } ) )
        self.sigil_points = sigil_points

