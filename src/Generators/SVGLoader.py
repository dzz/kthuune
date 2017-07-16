import xml.etree.ElementTree as ET

def get_edges(data, width, height ):

    def propkey(key):
        ns = "{http://www.librecad.org}"
        pk = "{0}{1}".format(ns,key)
        return pk

    root = ET.fromstring(data)
    all_lines = []
    pstart = []
    estart = []
    for layer in root.findall('./*'):
        layername = layer.attrib[propkey('layername')]
        print(layername)
        if(layername == "player_start"):
            print("PARSING PLAYER START")
            for circle in layer.findall('./*'):
                pstart = [ float(circle.attrib['cx']), float(circle.attrib['cy']) ]

        if(layername == "elder_start"):
            print("PARSING PLAYER START")
            for circle in layer.findall('./*'):
                estart = [ float(circle.attrib['cx']), float(circle.attrib['cy']) ]

        if(layername == "full_occluders"):
            print("PARSING OCCLUDERS")
            for line in layer.findall('./*'):
                all_lines.append( [ 
                                    [ float(line.attrib['x1']), float(line.attrib['y1']) ],
                                    [ float(line.attrib['x2']), float(line.attrib['y2']) ],
                                ])

    max_x = 0.0
    max_y = 0.0

    for line in all_lines:
        if line[0][0] > max_x: max_x = line[0][0]
        if line[1][0] > max_x: max_x = line[1][0]
        if line[0][1] > max_y: max_y = line[0][1]
        if line[1][1] > max_y: max_y = line[1][1]
        
    max_c = max(max_x,max_y)

    nfact_x = (1.0/max_c) * width
    nfact_y = (1.0/max_c) * height
    for line in all_lines:
        line[0][0] = (line[0][0]*nfact_x) - (width/2)
        line[0][1] = (line[0][1]*nfact_y) - (height/2)
        line[1][0] = (line[1][0]*nfact_x) - (width/2)
        line[1][1] = (line[1][1]*nfact_y) - (height/2)

    pstart[0] = (pstart[0] * nfact_x) - (width/2)
    pstart[1] = (pstart[1] * nfact_y) - (height/2)
    estart[0] = (estart[0] * nfact_x) - (width/2)
    estart[1] = (estart[1] * nfact_y) - (height/2)
    return { "all_lines" : all_lines, "player_start" : pstart, "elder_start" : estart }
