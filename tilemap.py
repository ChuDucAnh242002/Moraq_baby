import json, math

from core_funcs import *

def tuple_to_str(tp):
    return ';'.join([str(v) for v in tp])

def str_to_tuple(s):
    return tuple([int(v) for v in s.split(';')])

class Tilemap():
    def __init__(self, tile_size, view_size):
        self.tile_size = tuple(tile_size)
        self.view_size = tuple(view_size)
        self.tile_map = {}
        self.all_layers = []

    
