from core_funcs import *
from entity import BOOK_NAMES, ITEM_NAMES, Tile, Book, Item

FILE_NAMES = ['grass', 'dirt', 'chair_pillar', 'ladder', 'pillar_0', 'pillar_1', 'table_pillar']
CATEGORIES = [[Book, "books", BOOK_NAMES], [Item, "items", ITEM_NAMES]]

def tuple_to_str(tp):
    return ';'.join([str(v) for v in tp])

def str_to_tuple(s):
    return tuple([int(v) for v in s.split(';')])

class Tilemap():
    def __init__(self, level):
        self.map_image = self.init_map_image()
        self.total_level = level
        self.cur_level = 1

        # Map
        self.game_map = load_dict_map_json('assets/map/', self.total_level)
        self.game_map_entity = load_dict_entity('assets/map/', self.total_level)
        self.cur_map = self.game_map[self.cur_level]
        self.cur_entity = self.game_map_entity[self.cur_level]
        self.tile_size = self.map_image[1].get_width()

        # Chunk
        self.chunk_x, self.chunk_y = 15, 24
        self.tile_chunk = self.init_tile_chunk(self.chunk_x, self.chunk_y)
        self.entity_chunk = self.init_tile_entity((self.chunk_x - 1) * self.tile_size, (self.chunk_y - 1) * self.tile_size)

        # Tile and entity
        
        self.tiles = self.init_tiles()
        self.entities = self.init_entities(CATEGORIES)

    def init_map_image(self):
        map_image = {}
        for index, file_name in enumerate(FILE_NAMES):
            img_path = 'assets/images/pillar/' + file_name
            map_image[index] = load_image(img_path)
        return map_image

    def init_tile_chunk(self, max_row, max_col):
        tile_chunk = []
        for row in range(max_row):
            rows = []
            for col in range(max_col):
                rows.append(self.cur_map[row][col])
            tile_chunk.append(rows)
        return tile_chunk

    def init_tile_entity(self, max_row, max_col):
        entity_chuck = []
        for entity in self.cur_entity:
            x = entity["x"] - entity["originX"]
            y = entity["y"] - entity["originY"]
            if x < max_col and y < max_row:
                entity_chuck.append(entity)
        return entity_chuck

    def init_tiles(self):
        tiles = []
        for row, data_x in enumerate(self.tile_chunk):
            for col, index in enumerate(data_x):
                if index != -1:
                    tile = Tile(col * self.tile_size, row * self.tile_size, index, self.map_image[index])
                    tiles.append(tile)
        return tiles

    def init_entities(self, categories):
        # category example: (Book, books, names), (Item, items)
        entities = {}
        for category in categories:
            items = []
            type = category[0]
            type_name = category[1]
            names = category[2]
            for entity in self.entity_chunk:
                name = entity["name"]
                x = entity["x"] - entity["originX"]
                y = entity["y"] - entity["originY"]
                if name in names:
                    item = type(x, y, name)
                    items.append(item)
            if type_name not in entities:
                entities[type_name] = items
        return entities

    def move_chuck(self,player_x, player_y):
        if player_x > (self.chunk_x - 1) * self.tile_size:
            self.chunk_x += 15
        if player_y > (self.chunk_y - 1) * self.tile_size:
            self.chunk_y += 24
        self.tile_chunk = self.init_tile_chunk(self.chunk_x, self.chunk_y)
        self.entity_chunk = self.init_tile_entity((self.chunk_x - 1) * self.tile_size, (self.chunk_y - 1) * self.tile_size)


    def change_level(self, level):
        self.cur_level = level
        self.cur_map = self.game_map[self.cur_level]
        self.cur_entity = self.game_map_entity[self.cur_level]
        self.tile_chunk = self.init_tile_chunk(15, 24)
        self.entity_chunk = self.init_tile_entity((self.chunk_x - 1) * self.tile_size, (self.chunk_y - 1) * self.tile_size)
        self.tiles = self.init_tiles()
        self.entities = self.init_entities([[Book, "books", BOOK_NAMES], [Item, "items", ITEM_NAMES]])

    
