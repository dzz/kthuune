from random import uniform, choice
from math import hypot
from Newfoundland.Object import Object
from Beagle import API as BGL
from math import sin,cos,pi
from .txt_specs import *
import random

class Fire(Object):
        def __init__(self,**kwargs):
            overrides = {
                    'texture' : None,
                    'tick_type' : Object.TickTypes.TICK_FOREVER,
                    'light_radius' : 125.0,
                    'light_type' : Object.LightTypes.DYNAMIC_SHADOWCASTER
                }
            overrides.update(kwargs)
            Object.__init__(self,**overrides)
            self.base_p = self.p
            self.base_radius = self.light_radius

        def tick(self):
            rad_jitter = uniform(0.8,1.2)
            self.light_radius = (self.light_radius*0.9)+(self.base_radius * rad_jitter*0.1)
            jitter = [uniform(-1.2,1.2), uniform(-1.2,1.2) ]
            np = [ self.base_p[0] + jitter[0], self.base_p[1]+jitter[1] ]
            self.p = [ np[0]*0.02 + self.p[0]*0.98,np[1]*0.02 + self.p[1]*0.98 ]
            ncolor = [ uniform(0.6,0.9), uniform(0.3,0.6), uniform(0.1,0.3),1.0]
            for i in range(0,4):
                self.color[i] = self.color[i]*0.9+ncolor[i]*0.1

            return True

        def render(self):
            return



class TreeTop(Object):
        def __init__(self,**kwargs):
            overrides = {
                    "num" : 0,
                    "texture" : choice( [
                            BGL.assets.get("KT-forest/texture/treetop"),
                            BGL.assets.get("KT-forest/texture/treetop2") ] ),
                    'tick_type' : Object.TickTypes.TICK_FOREVER,
                    'size' : [ 5.0,5.0],
                    'rad' : uniform(-3.14,3.14),
                    'parallax' : 1.2,
                    'z_index' : 100,
                    'wind_speed' : uniform(0.01,0.2),
                    'wind_mod' : uniform(1.1,1.2)
                }
            overrides.update(kwargs)
            Object.__init__(self,**overrides)
            self.t = 0
            self.base_size = [ self.size[0], self.size[1] ]
            self.draw_color = [0.8,uniform(0.0,1.0),0.8,uniform(0.8,1.0)]

        def tick(self):
            self.t = self.t + 0.01
            self.size[0] = self.base_size[0] * ( 4.0 + (1.5*(sin(self.t* self.wind_speed))))
            self.size[1] = self.base_size[1] * ( 4.0 + (1.5*(cos(self.t* self.wind_speed*self.wind_mod))))
            return True

        def should_draw(self):
            p = self.get_shader_params()['translation_world']
            visRad = 70
            if(p[0]<-visRad): return False
            if(p[1]<-visRad): return False
            if(p[0]>visRad): return False
            if(p[1]>visRad): return False
            return True

        def get_shader_params(self):
            params = Object.get_shader_params(self)
            tw = params["translation_world"]
            tw[0] = tw[0]*self.parallax
            tw[1] = tw[1]*self.parallax
            params["translation_world" ] = tw
            params["filter_color"] = self.draw_color
            return params

class TreeRoots(Object):
        def __init__(self,**kwargs):
            overrides = {
                    "num" : 0,
                    "texture" : BGL.assets.get("KT-forest/texture/treeroots"),
                    'tick_type' : Object.TickTypes.TICK_FOREVER,
                    'size' : [ 5.0,5.0],
                    'rad' : uniform(-3.14,3.14),
                    'z_index' : -100,
                }
            overrides.update(kwargs)
            Object.__init__(self,**overrides)
            self.t = 0
            self.base_size = [ self.size[0], self.size[1] ]
            self.draw_color = [0.8,uniform(0.0,1.0),0.8,uniform(0.6,0.7)]

        def should_draw(self):
            p = self.get_shader_params()['translation_world']
            visRad = 100
            if(p[0]<-visRad): return False
            if(p[1]<-visRad): return False
            if(p[0]>visRad): return False
            if(p[1]>visRad): return False
            return True

        def get_shader_params(self):
            params = Object.get_shader_params(self)
            tw = params["translation_world"]
            params["translation_world" ] = tw
            params["filter_color"] = self.draw_color
            return params

class TreeShadow(Object):
        def __init__(self,**kwargs):
            self.scale = 12
            tt = kwargs['TreeTop']
            overrides = {
                    "num" : 0,
                    "texture" : BGL.assets.get("KT-forest/texture/treetop"),
                    'tick_type' : Object.TickTypes.TICK_FOREVER,
                    'size' : [ self.scale*tt.size[0],self.scale*tt.size[1]],
                    'rad' : tt.rad,
                    'z_index' : -100,
                    'tt' : tt
                }
            overrides.update(kwargs)
            Object.__init__(self,**overrides)
            self.t = 0
            self.base_size = [ self.size[0], self.size[1] ]
            self.draw_color = [0.8,uniform(0.0,1.0),0.8,uniform(0.3,0.4)]

        def should_draw(self):
            p = self.get_shader_params()['translation_world']
            visRad = 150
            if(p[0]<-visRad): return False
            if(p[1]<-visRad): return False
            if(p[0]>visRad): return False
            if(p[1]>visRad): return False
            return True

        def get_shader_params(self):

            params = Object.get_shader_params(self)
            tw = params["translation_world"]
            params["translation_world" ] = tw
            params["filter_color"] = self.draw_color
            return params

def map_txt_spec( df, txt_spec_raw, probability, times, jitter, effect  ):

    txt_spec = random.sample(txt_spec_raw, len(txt_spec_raw))
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

    def compile(self, dungeon_floor, base_objects ):
        self.objects = []
        if(base_objects):
            self.objects.extend(base_objects)

        self.generate_sigil_points( dungeon_floor )
        #self.generate_trees( dungeon_floor )
        self.generate_photon_emitters(dungeon_floor)

        #self.light_occluders = self.tree_occluders
        self.light_occluders = []

        self.map_edges = self.gen_edges( dungeon_floor )
        self.light_occluders = []
        self.light_occluders.extend( self.map_edges )

        self.generate_inner_trees(dungeon_floor)
        self.generate_edge_trees()
        self.generate_static_lights(dungeon_floor)
        self.generate_fires(dungeon_floor)
        self.generate_tiledata(  dungeon_floor )

    def generate_fires(self,df):
        for pobj in filter( lambda x: "portal_target" in x.__dict__, self.objects):
            self.objects.append( Fire( p=pobj.p) )


    def generate_inner_trees(self,df):

        self.tree_pts = []
        occluders = []
        for t in range(0,25):
            print("MAKING TREE")
            px,py = uniform(-df.width,df.width),uniform(-df.height,df.height)
            px*=0.4
            py*=0.4
            rad = uniform(3.2,6.3)
            occluders.extend( self.gen_rand_circle_lines( 0.5,1.5, rad, [px,py]))

            size = uniform(1.0,8.0)
            plx = uniform(2.2,3.8)

            self.tree_pts.append([px,py])
            pobjs = filter( lambda x: "portal_target" in x.__dict__, self.objects)
            for tt in range(2,choice(range(4,5))):
                valid = False
                while not valid:
                    valid = True
                    min_dist = 25
                    p = [px+uniform(-3.0,3.0),py+uniform(-3.0,3.0)]
                    for obj in pobjs:
                        if hypot( p[0]-obj.p[0], p[1]-obj.p[1])<min_dist: 
                            valid = False
                            break

                tt = TreeTop( p=p, size=[size,size],parralax = plx) 
                self.objects.append( tt )
                #tt.visible = False
                self.objects.append( TreeShadow(p=p, TreeTop=tt) )
                size = size * uniform(1.2,1.5)
                plx = plx * uniform(1.1,1.3)

            for tt in range(2,choice(range(2,5))):
                size = uniform(10.0,40.0)
                p = [px+uniform(-2.0,2.0),py+uniform(-2.0,2.0)]
                self.objects.append( TreeRoots( p=p, size=[size,size]) )
            #    if(choice([True,False])):
            #        self.objects.append( TreeShadow( p=p, size=[size*2,size*2]) )


            ##for tt in range(2,choice(range(3,15))):
            ##    p = [px+uniform(-3.0,3.0),py+uniform(-3.0,3.0)]
            ##    self.objects.append( TreeTop( p=p, size=[size,size],parralax = plx) )
            ##    size = size * uniform(1.2,1.5)
            ##    plx = plx * uniform(1.2,1.5)

        self.light_occluders.extend(occluders)


    def generate_edge_trees(self):
        for edge in self.map_edges:
            for x in range(0,choice(range(4,20))):
                size = uniform(2.0,8.0)
                dx = edge[1][0] - edge[0][0]
                dy = edge[1][1] - edge[0][1]
                d = uniform(0.0,1.0)
                px,py = d*dx,d*dy
                x,y = edge[0][0]+px,edge[0][1]+py
                p = [x,y]
                if(uniform(0.0,1.0)>0.7):
                    self.tree_pts.append(p)
                self.objects.append( TreeTop( p=p, size=[size,size],parralax = uniform(1.1,1.8)) )




    def get_objects(self):
        return self.objects


    def gen_rand_circle_lines(self,min_step,max_step,rad, p=[0.0,0.0]):
        r = -pi
        points = []
        dfilt = None
        while(r < pi):
            r = r + uniform(min_step,max_step)
            #rad = min(df.width,df.height)*0.5
            d = uniform(0.5*rad, 1.0*rad)
            if dfilt is None:
                dfilt = d
            else:
                dfilt = (d*0.2)+(dfilt*0.8)
            points.append( [ (cos(r)*dfilt)+p[0], (sin(r)*dfilt)+p[1] ] )


        lines = []
        for i in range(0, len(points)-1):
            lines.append( [ points[i],points[i+1]] )

        lines.append( [ points[len(points)-1],points[0]] )
        return lines

    def gen_edges(self, df):
        return self.gen_rand_circle_lines( 0.01,0.2, min(df.width,df.height)*0.5)
        ## r = 0.0
        ## points = []
        ## dfilt = None
        ## while(r < 2*pi):
        ##     r = r + uniform(0.01,0.2)
        ##     rad = min(df.width,df.height)*0.5
        ##     d = uniform(0.5*rad, 1.0*rad)
        ##     if dfilt is None:
        ##         dfilt = d
        ##     else:
        ##         dfilt = (d*0.2)+(dfilt*0.8)
        ##     points.append( [ cos(r)*dfilt, sin(r)*dfilt ] )


        ### lines = []
        ### for i in range(0, len(points)-1):
        ###     lines.append( [ points[i],points[i+1]] )

        ### lines.append( [ points[len(points)-1],points[0]] )
        ## lines = [
        ##     [ [-0.5*df.width, -0.5*df.height],[0.5*df.width, -0.5*df.height] ],
        ##     [ [ 0.5*df.width, -0.5*df.height],[0.5*df.width, 0.5*df.height] ],
        ##     [ [0.5*df.width, 0.5*df.height],[-0.5*df.width, 0.5*df.height] ],
        ##     [ [-0.5*df.width, 0.5*df.height],[-0.5*df.width, -0.5*df.height] ]
        ## ]
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


    
    def evaluate_tile(self,rx,ry):

        win_d = 0
        win_range = None 
        second_range = None
        for pt in self.vpts:
            d = hypot(rx-pt[1], ry-pt[2])
            if win_range is None:
                win_d = d
                win_range = pt[0]
                second_range = win_range
            else:
                if( d< win_d):
                    win_d = d
                    second_range = win_range
                    win_range = pt[0]

        
        return choice( choice([win_range, second_range]) )
                 

    
    def generate_voroni_pts(self):
        self.vpts = []

        self.width = self.df.width #i give up
        self.height = self.df.height

        for pt in self.tree_pts:
            self.vpts.append( ( (1,10) , pt[0], pt[1] ) )

        #for x in range(0,50):
        #    self.vpts.append( ( (1,1) , uniform(-self.width, self.width), uniform(-self.height, self.height)) )

        for pobj in filter( lambda x: "portal_target" in x.__dict__, self.objects):
            self.vpts.append( ( (11,19) , pobj.p[0], pobj.p[1] ) )

        for i in range(0,8):
            self.vpts.append(((5,15) , uniform(-self.width, self.width), uniform(-self.height,self.height)))




    def generate_tiledata( self, df ):

        self.df = df #i give up
        self.generate_voroni_pts()

        tile_data = [0]*(df.width*df.height)
        for x in range(0, df.width):
            for y in range(0, df.height):
                ####### closest_sigil_point = None
                ####### score = None
                ####### for sigil_point in self.sigil_points:

                #######     a =sigil_point["p"][0]-x
                #######     b =sigil_point["p"][1]-y
                #######     d = abs(a) + abs(b)
                #######     if not score:
                #######         score = d
                #######         closest_sigil_point = sigil_point
                #######     elif d < score:
                #######         closest_sigil_point = sigil_point
                #######         score = d
                ####### tile_data[  (y * df.width) + x ]  = self.get_sigil_tiledata(closest_sigil_point["sigil"])

                rx = float(x*2)-(df.width)
                ry = float(y*2)-(df.height)

                tval = self.evaluate_tile(rx,ry)
                tile_data[  (y * df.width) + x ]  = tval

        self.tile_data = tile_data

    def generate_static_lights(self, df):
        static_lights = []
        # txt_spec = [
        #     [ "  1     1  " ],
        #     [ " 2   3   2 " ],
        #     [ "  1     1  " ]
        # ]

        txt_spec = choice(light_specs)

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


        for x in range(0,25):
            p = [ uniform(-0.5,0.5)*df.width, uniform(-0.5,0.5)*df.height ]
            static_lights.extend( generate_light(choice(['1','2','3']),p) )
        #map_txt_spec( df, txt_spec, 1.0, 2, 25.0, lambda char, p : static_lights.extend(generate_light(char, p)))
        self.objects.extend( static_lights )


    def generate_photon_emitters(self, df):
        photon_emitters = []
        txt_spec = choice( photon_specs )
        ##txt_spec = [
        ##    [ "2,,,,,,2" ],
        ##    [ ",2,11,2," ],
        ##    [ ",1,13,1," ],
        ##    [ "3,1113,3" ],
        ##    [ "1,,31,2," ],
        ##    [ ",2,11,2," ],
        ##    [ "2,,1,,,2" ]
        ## ]

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
        ##txt_spec = [
        ##    [ "Q Q Q Q Q Q Q Q Q Q" ],
        ##    [ "Q _ _`_ _ _ ` _ _ Q" ],
        ##    [ "Q_ ee` yyyy_`_ee _Q" ],
        ##    [ "Q_ ee` yyyy_`_ee _Q" ],
        ##    [ "Q_ _ ` ` ` ``Q _ _Q" ],
        ##    [ "Q_ ee_y_ _y_ _ee _Q" ],
        ##    [ "Q_ ee_ _ ` _ yee _Q" ],
        ##    [ "Q_ _ y _ ` _ ___y_Q" ],
        ##    [ "Q_ ee_ _Q` _ _ee _Q" ],
        ##    [ "Q_ ee_ _ ` _ _ee _Q" ],
        ##    [ "Q_ _ _y_ ` y _ _ _Q" ],
        ##    [ "Q Q Q Q Q Q Q Q Q Q" ] ]
        txt_spec = choice(tree_specs)

        tree_occluders = []

        def generate_tree_objects(char,p):
            size = None
            if char == "Q":
                size = uniform(5,15)
            if char == "e":
                size = uniform(3,7)
            if char == "`":
                size = uniform(2,5)
            if(size is None):
                return []
            p[0] = p[0]-(df.width/2) + uniform(-1.0,1.0)
            p[1] = p[1]-(df.height/2) + uniform(-1.0,1.0)


            self.tree_pts.append(p)
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
            points.append( [ 0.5*size, -0.5*size ] )
            points.append( [ size, 0.0 ] )
            points.append( [ 0.5*size, 0.5*size ] )
            points.append( [ 0.0, 1*size ] )
            points.append( [ -0.5*size, 0.5*size ] )
            points.append( [ -1*size, 0.0 ] )
            points.append( [ -0.5*size, -0.5*size ] )

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

        map_txt_spec( df, txt_spec, 1.0, 2, 2.0, lambda char, p : tree_occluders.extend(generate_tree_occluders(char, p)))
        self.tree_occluders = tree_occluders

    def generate_sigil_points( self, df):
        #txt_spec = [
        #    [ "# # # # # # # # # #" ],
        #    [ "# _ _`_ _ _ ` _ _ #" ],
        #    [ "#_ XX` yyyy_`_XX _#" ],
        #    [ "#_ XX` yyyy_`_XX _#" ],
        #    [ "#_ _ ` ` ` ``_ _ _#" ],
        #    [ "#_ XX_ _ _ _ _XX _#" ],
        #    [ "#_ XX_ _ ` _ _XX _#" ],
        #    [ "#_ _ _ _ ` _ ___ _#" ],
        #    [ "#_ XX_ _ ` _ _XX _#" ],
        #    [ "#_ XX_ _ ` _ _XX _#" ],
        #    [ "#_ _ _ _ ` _ _ _ _#" ],
        #    [ "# # # # # # # # # #" ] ]

        txt_spec = choice( sigil_specs )
        sigil_points = []

        map_txt_spec( df, txt_spec, 0.8, 2, 1.0, lambda char, p : sigil_points.append({ "sigil": char, "p": p } ) )
        self.sigil_points = sigil_points
