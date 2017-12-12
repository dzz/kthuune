from random import uniform, choice
from math import hypot
from Newfoundland.Object import Object
from Beagle import API as BGL
from math import sin,cos,pi
from .txt_specs import *
import random

class BasicGenerator():
    def __init__(self):
        pass

    def compile(self, dungeon_floor, base_objects ):

        self.objects = []
        if(base_objects):
            self.objects.extend(base_objects)

        self.light_occluders = []
        self.photon_emitters = []
        self.df = dungeon_floor

    def get_tiledata(self):
        df = self.df
        tiles = [1]*(df.width*df.height)
        return tiles

    def get_light_occluders(self):
        return self.light_occluders

    def get_photon_emitters(self):
        return self.photon_emitters

    def get_objects(self):
        return self.objects
