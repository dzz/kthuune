class Edges:
    def get_h_lines(brushes):
        h_lines = []
        for brush in brushes:
            h_lines.append([ brush.y1,brush.x1, brush.x2 ])
            h_lines.append([ brush.y2,brush.x1, brush.x2 ])
        return h_lines

    def get_v_lines(brushes):
        v_lines = []
        for brush in brushes:
            v_lines.append([ brush.x1,brush.y1, brush.y2 ])
            v_lines.append([ brush.x2,brush.y1, brush.y2 ])
        return v_lines

    def make_edges( area, brush, brushes):

        check_brushes = list(filter(lambda b: b is not brush, brushes))
        h_lines = Edges.get_h_lines(check_brushes)
        v_lines = Edges.get_v_lines(check_brushes)

        traced_lines = []

        def h_line_to_trace(y, line):
            return [ line[0],y,line[1],y ]

        def v_line_to_trace(x, line):
            return [ x,line[0], x,line[1] ]

        #trace top and bottom
        for y in [ brush.y1, brush.y2 ]:
            line = [ brush.x1, brush.x1 ]
            for x in range(brush.x1, brush.x2+1):
                potential_conflicts = list(filter(lambda l: l[0] == y,h_lines))
                if len(potential_conflicts)==0:
                    line[1] = x
                for pc in potential_conflicts:
                    if(x>pc[1]) and (x<=pc[2]):
                        if(line[0]!=line[1]):
                            traced_lines.append(h_line_to_trace(y,line))
                        line[0] = x
                        line[1] = x 
                    else:
                        line[1] = x
            if(line[0]!=line[1]):
                traced_lines.append(h_line_to_trace(y,line))

        #trace left and right
        for x in [ brush.x1, brush.x2 ]:
            line = [ brush.y1, brush.y1 ]
            for y in range(brush.y1, brush.y2+1):
                potential_conflicts = list(filter(lambda l: l[0] == x,v_lines))
                if len(potential_conflicts)==0:
                    line[1] = y
                for pc in potential_conflicts:
                    if(y>pc[1]) and (y<=pc[2]):
                        if(line[0]!=line[1]):
                            traced_lines.append(v_line_to_trace(x,line))
                        line[0] = y
                        line[1] = y 
                    else:
                        line[1] = y
            if(line[0]!=line[1]):
                traced_lines.append(v_line_to_trace(x,line))
        return traced_lines


class TestBrush:
    pass

if __name__ == "__main__":
    print("No occlusion")
    test_brush = TestBrush()
    test_brush.x1 = -4
    test_brush.x2 = 4
    test_brush.y1 = -4
    test_brush.y2 = 4
    brushes = [ test_brush ] 
    print(Edges.make_edges( None, test_brush, brushes))

    print("top occluded from -2 > +2")
    test_brush1 = TestBrush()
    test_brush1.x1 = -4
    test_brush1.x2 = 4
    test_brush1.y1 = -4
    test_brush1.y2 = 4
    test_brush2 = TestBrush()
    test_brush2.x1 = -2
    test_brush2.x2 = 2
    test_brush2.y1 = -8
    test_brush2.y2 = -4
    brushes = [ test_brush1, test_brush2 ] 
    print(Edges.make_edges( None, test_brush1, brushes))

    print("bottom occluded from -3 > +3")
    test_brush1 = TestBrush()
    test_brush1.x1 = -4
    test_brush1.x2 = 4
    test_brush1.y1 = -4
    test_brush1.y2 = 4
    test_brush2 = TestBrush()
    test_brush2.x1 = -3
    test_brush2.x2 = 3
    test_brush2.y1 = 4
    test_brush2.y2 = 8
    brushes = [ test_brush1, test_brush2 ] 
    print(Edges.make_edges( None, test_brush1, brushes))

    print("bottom and top totally occluded")
    test_brush1 = TestBrush()
    test_brush1.x1 = -4
    test_brush1.x2 = 4
    test_brush1.y1 = -4
    test_brush1.y2 = 4
    test_brush2 = TestBrush()
    test_brush2.x1 = -4
    test_brush2.x2 = 4
    test_brush2.y1 = -4
    test_brush2.y2 = 4
    brushes = [ test_brush1, test_brush2 ] 
    print(Edges.make_edges( None, test_brush1, brushes))


