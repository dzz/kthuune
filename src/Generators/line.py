def fill_scanline( scanline ):
    converted = [None] * len(scanline)
    history = []

    for x in range(0, len(scanline)):
        cell = scanline[x]
        if cell is None:
            if len(history) is 0:
                converted[x] = 0
            else:
                converted[x] = history[-1]
        else:
            converted[x] = cell
            if len(history) is not 0:
                if history[-1] == cell:
                    history.pop()
                else:
                    history.append(cell)
            else:
                history.append(cell)
    return converted


def vscan_line(start, end):
    pts = [ start, end ]
    if (end[1]-start[1]) == 0:
        return pts
    dx = (float(end[0])-float(start[0])) / (float(end[1])-float(start[1]))
    
    for y in range(int(start[1]),int(end[1])):
        idx = y - start[1]
        x = idx * dx
        pts.append((int(x),int(y)))

    return pts

magic_scanline = [ None, None, None, 1, 1, 1, 2, None, None, 2, None, None, 1, None, None ]
print(fill_scanline(magic_scanline))
print(vscan_line((-10,0),(10,0)))
print(vscan_line((-10,-10),(10,10)))
print(vscan_line((0,-10),(0,10)))
print(vscan_line((0,-10),(3,10)))

