#!/usr/bin/python2
from random import uniform, choice

def make(cls, attrs):
    inst = cls()
    for key in attrs:
        inst.__dict__[key] = attrs[key]
    return inst

class area():
    min_portals = 2
    max_portals = 3
    def __init__(self, gen_portals = True ):
        self.depth = 0
        self.ring = 0
        self.portals = []
        if(gen_portals):
            self.generate_portals()

    def generate_portals(self):
        for x in range(0,choice(range(area.min_portals,area.max_portals))):
            p = make(portal, { "left_area":self, "left_p":self.get_random_portal_point()})
            self.portals.append(p)

    def spawn_children(self):
        children = []
        for portal in list(filter(lambda x: x.right_area is None, self.portals)):
            child = make(area,{})
            children.append(child)
            portal.right_area = child
            portal.right_p = child.get_random_portal_point()
        return children

    def get_random_portal_point(self):
        return [ uniform(-100,100), uniform(-100,100)]

class portal():
    def __init__(self):
        self.left_area = None
        self.left_p = [0,0]
        self.right_area = None
        self.right_p = [0,0]



def reduce_areas(areas, amt = 0.75):
    reduced_areas = []
    merge_sets = []
    cur_set = []
    first = True
    for a in areas:
        cur_set.append(a)
        if(uniform(0.0,1.0)<amt) or first:
            merge_sets.append(cur_set)
            cur_set = []
        first = False
    for merge_set in merge_sets:
        merged_area = area( gen_portals = False )
        for a in merge_set:
            for p in a.portals:
                merged_area.portals.append(p)
                p.right_area = merged_area
                if(p.right_area is None):
                    merged_area.portals.remove(p)
        reduced_areas.append(merged_area)
    return reduced_areas

def reduce_layer(areas, layer, amount):
    reduced_layer = reduce_areas( list(filter(lambda x: x.depth==layer, areas)),amount)
    areas = list(filter(lambda x: x.depth != layer, areas))
    for a in reduced_layer: a.depth = layer
    areas.extend(reduced_layer)
    areas.sort( key=lambda x:x.depth )
    return areas

def generate_tunnels(areas, amount = 0.33):
    #only make tunnels between adjacent rings
    areas.sort( key=lambda x:x.ring)
    ntuns = int(len(areas)*amount)
    for x in range(0,ntuns):
        source_idx = choice(range(0,len(areas)))
        if(source_idx == (len(areas)-1)):
            source_idx = len(areas)-2
        target_idx = source_idx+1
        sa = areas[source_idx]
        ta = areas[target_idx]
        sa.portals.append( make(portal, { "left_area" : sa, "left_p" : sa.get_random_portal_point(), "right_area" : ta, "right_p" : ta.get_random_portal_point() } ))

def make_portals_bidirectional(areas):
    tportals = []
    for a in areas:
        tportals.extend(a.portals)

    for p in tportals:
        p.right_area.portals.append(p)


class genparams():
    max_depth = 6

def generate_areas():
    layer = 0
    max_depth = genparams.max_depth
    root_area = make( area, { "ring" : 1})

    areas = [ root_area ]
    while layer < max_depth:
        for a in areas:
            a.depth = a.depth + 1
        for a in list(filter(lambda x: x.depth == 1, areas )):
            areas.extend( a.spawn_children())
        layer = layer + 1

    areas = reduce_layer(areas, 0, 0.1)
    areas = reduce_layer(areas, 1, 0.2)
    areas = reduce_layer(areas, 2, 0.8)
    areas = reduce_layer(areas, 3, 1.0)
    areas = reduce_layer(areas, 4, 1.0)
    areas = reduce_layer(areas, 5, 0.0)

    for l in range(0, max_depth):
        layer_areas = list(filter(lambda x:x.depth==l, areas))
        ring_size = len(layer_areas)//2
        dbg_rings = []
        for idx, a in enumerate(layer_areas):
            a.ring = idx-ring_size
            dbg_rings.append(a.ring)

        if l is not 0:
            generate_tunnels(layer_areas)

    make_portals_bidirectional(areas)
    return areas

def show_layers(areas):
    for l in range(0, genparams.max_depth):
        layer_areas = list(filter(lambda x:x.depth==l, areas))
        print(len(layer_areas), list(map(lambda x:x.ring,layer_areas)))

def generate_qualified_areas():
    def qualify(areas):
        top_areas = list(filter(lambda x:x.depth==0, areas))

        if len(top_areas) not in [12,14,16]:
            return False
        return True

    areas = generate_areas()
    while not qualify(areas):
        areas = generate_areas()

    return areas
