from .PolyFillList import PolyFillList

class Remesher:
    def __init__(self):
        pass

    def find_limits(self, meshable):
        left = right = top = bottom = 0
        for brush in meshable:
            left = min(left,brush.x1)
            right = max(right,brush.x2)
            top = min(top,brush.y1)
            bottom = max(bottom,brush.y2)
        self.left, self.right, self.top, self.bottom = left,right,top,bottom

    def remesh( self, brushes, key ):

        meshable = list(filter( lambda brush: PolyFillList.getPolyFill(brush.polyfill_key).mesh_key == key , brushes))

        self.find_limits(meshable)

        grid = {}
        for x in range( self.left, self.right):
            for y in range(self.top, self.bottom):
                for brush in meshable:
                    if (x>=brush.x1) and (x<brush.x2) and (y>=brush.y1) and (y<brush.y2):
                        grid[(x,y)] = True

        traced = []
        for x in range( self.left, self.right):
            for y in range(self.top, self.bottom):
                if (x,y) in grid:
                    if(x,y-1) not in grid:
                        traced.append( [ x, y, x+1, y ] )
                    if(x,y+1) not in grid:
                        traced.append( [ x, y+1, x+1, y+1 ] )
                    if(x-1,y) not in grid:
                        traced.append( [x,y,x,y+1] )
                    if(x+1,y) not in grid:
                        traced.append( [x+1,y,x+1,y+1] )
        print(traced)
        return traced 
