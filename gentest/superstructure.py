#!/usr/bin/python2




class world():
    depth = 7

class layer():
    pass

class area():
    def __init__(self, level):
        self.links = []
        self.level = level

class link():
    pass


root = area( level = world.depth )

