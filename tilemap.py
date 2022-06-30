# import pygame
# import json, math

from core_funcs import *

FILE_NAMES = ['grass', 'dirt', 'chair_pillar', 'ladder', 'pillar_0', 'pillar_1', 'table_pillar']

def tuple_to_str(tp):
    return ';'.join([str(v) for v in tp])

def str_to_tuple(s):
    return tuple([int(v) for v in s.split(';')])

class Tilemap():
    def __init__(self, level):
        self.map_image = self.init_map_image()
        self.total_level = level
        self.game_map = load_dict_map_json('assets/map/', self.total_level)
        self.game_map_entity = load_dict_entity('assets/map/', self.total_level)
        self.tile_size = self.map_image[1].get_width()

    def init_map_image(self):
        map_image = {}
        for index, file_name in enumerate(FILE_NAMES):
            if index == 0 or index == 1:
                img_path = 'assets/images/' + file_name
            if index >= 2 and index <= 6:
                img_path = 'assets/images/pillar/' + file_name
            map_image[index + 1] = load_image(img_path)
        return map_image

    
