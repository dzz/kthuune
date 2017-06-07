from random import uniform, choice
from math import hypot
from Newfoundland.Object import Object
from Beagle import API as BGL
from math import sin,cos

class TreeTop(Object):
        def __init__(self,**kwargs):
            overrides = {
                    "num" : 0,
                    "texture" : BGL.assets.get("KT-forest/texture/treetop"),
                    'tick_type' : Object.TickTypes.TICK_FOREVER,
                    'size' : [5.0,5.0],
                    'rad' : uniform(-3.14,3.14),
                    'parallax' : 1.2,
                    'z_index' : 100,
                    'wind_speed' : uniform(0.01,0.03),
                    'wind_mod' : uniform(1.1,1.2)
                }
            overrides.update(kwargs)
            Object.__init__(self,**overrides)
            self.t = 0

        def tick(self):
            self.t = self.t + 0.01
            self.size[0] = self.size[0] + (sin(self.t* self.wind_speed)*0.01)
            self.size[1] = self.size[1] + (cos(self.t* self.wind_speed*self.wind_mod)*0.01)
            return True

        def get_shader_params(self):
            params = Object.get_shader_params(self)
            tw = params["translation_world"]
            tw[0] = tw[0]*self.parallax
            tw[1] = tw[1]*self.parallax
            params["translation_world" ] = tw
            params["filter_color"] = [0.8,uniform(0.0,1.0),0.8,0.8]
            return params

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
        self.objects = []

        self.generate_sigil_points( dungeon_floor )
        self.generate_tiledata(  dungeon_floor )
        self.generate_trees( dungeon_floor )
        self.generate_photon_emitters(dungeon_floor)

        self.light_occluders = self.tree_occluders
        self.light_occluders.extend( self.get_base_occluders(dungeon_floor) )
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
        tile_data = [0]*(df.width*df.height)
        for x in range(0, df.width):
            for y in range(0, df.height):
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
                tile_data[  (y * df.width) + x ]  = self.get_sigil_tiledata(closest_sigil_point["sigil"])
                #tile_data[  (y * df.width) + x ]  = 1

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

            return [ Object( visible = False, light_type = style[0], p = p, light_radius=style[2], color = list( map( lambda x: x*0.8,style[1]))) ]

        map_txt_spec( df, txt_spec, 1.0, 2, 25.0, lambda char, p : static_lights.extend(generate_light(char, p)))
        self.objects.extend( static_lights )


    def generate_photon_emitters(self, df):
        photon_emitters = []
        txt_spec = [
            [ "2,,,,,,2" ],
            [ ",2,11,2," ],
            [ ",1,13,1," ],
            [ "3,1113,3" ],
            [ "1,,31,2," ],
            [ ",2,11,2," ],
            [ "2,,1,,,2" ]
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
            [ "Q_ _ ` ` ` ``Q _ _Q" ],
            [ "Q_ ee_y_ _y_ _ee _Q" ],
            [ "Q_ ee_ _ ` _ yee _Q" ],
            [ "Q_ _ y _ ` _ ___y_Q" ],
            [ "Q_ ee_ _Q` _ _ee _Q" ],
            [ "Q_ ee_ _ ` _ _ee _Q" ],
            [ "Q_ _ _y_ ` y _ _ _Q" ],
            [ "Q Q Q Q Q Q Q Q Q Q" ] ]

        tree_occluders = []

        def generate_tree_objects(char,p):
            size = None
            if char == "Q":
                size = uniform(10,25)
            if char == "e":
                size = uniform(5,10)
            if char == "`":
                size = uniform(3,7)
            if(size is None):
                return []
            p[0] = p[0]-(df.width/2) + uniform(-1.0,1.0)
            p[1] = p[1]-(df.height/2) + uniform(-1.0,1.0)
            return [ TreeTop( p = p, size = [ size*0.6, size*0.6 ], parallax = uniform(1.1,1.8) ) ]
            
        def generate_tree_occluders(char,p):
            size = None
            if char == "Q":
                size = uniform(3.5,16.2)
            if char == "e":
                size = uniform(1.3,5.6)
            if char == "`":
                size = 0.6


            if(size is None or uniform(0.0,1.0) < 0.5):
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

        tree_objects = []
        map_txt_spec( df, txt_spec, 0.9, 4, 5.0, lambda char, p : tree_objects.extend(generate_tree_objects(char, p)))
        tree_objects.sort( key =lambda x: x.parallax )
        self.objects.extend(tree_objects)

        map_txt_spec( df, txt_spec, 0.9, 1, 2.0, lambda char, p : tree_occluders.extend(generate_tree_occluders(char, p)))
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

