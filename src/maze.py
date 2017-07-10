from random import uniform, choice
from math import hypot,floor
#from Newfoundland.Object import Object
#from Beagle import API as BGL
from math import sin,cos,pi
#from .txt_specs import *
import random

def u(a,b): return uniform(a,b)

def ccw(A,B,C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

def make_maze(w,h):
    def closest_p(p,srch ):
        wind = None
        winp = None
        for tp in srch:
            d = hypot( tp[0]-p[0], tp[1]-p[1] )
            if(wind is None):
                winp = tp
                wind = d
            elif( d<wind):
                wind = d
                winp = tp
        return winp

    def make_test_spine(npts):
        pts = []
        for i in range(0,npts):
            pts.append( [ u(-w,w), u(-h,h) ] )

        sp = choice(pts)
        edge = [ sp ]
        while(len(pts)>0):
            np = closest_p(edge[-1],pts)
            pts.remove(np)
            edge.append(np) 
        return edge

    def make_spine():
        def validate_edge(edge):
            lines = []
            for i in range(0,len(edge)-1):
                line = [edge[i],edge[i+1]]
                lines.append(line)

            for line in lines:
                for test_line in lines:
                    if(test_line is not line):
                        shared_pt = False
                        for tpt in test_line:
                            for lpt in line:
                                if(lpt[0] == tpt[0]) and (lpt[1]==tpt[1]):
                                    shared_pt = True
                        if not shared_pt and intersect(line[0],line[1], test_line[0],test_line[1]):
                            print(line)
                            print(test_line)
                            return None
            return edge

        edge = None
        while edge is None:
            edge = make_test_spine(80)
            edge = validate_edge(edge)
        return edge

    edges = [make_spine()]
    return edges


maze = make_maze(100,100)

print('<svg height="300" width="300">')

cola = 0
colb = 0
colc = 0

for edge in maze:
    for i in range(0,len(edge)-1):
        line = [ edge[i], edge[i+1] ]
        print('<line x1="{0}" y1="{1}" x2="{2}" y2="{3}" style="stroke:rgb({4},{5},{6});stroke-width:2" />'.format(line[0][0]+150,line[0][1]+150,line[1][0]+150,line[1][1]+150,cola,colb,colc))
    cola = (cola + 16) % 256
    colb = (colb + 32) % 256
    colc = (colc + 64) % 256
print('</svg>')
