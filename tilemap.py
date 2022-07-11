from core_funcs import *
from entity import BOOK_NAMES, ITEM_NAMES, Tile, Book, Item

FILE_NAMES = ['grass', 'dirt', 'chair_pillar', 'ladder', 'pillar_0', 'pillar_1', 'table_pillar']
CATEGORIES = [[Book, "books", BOOK_NAMES], [Item, "items", ITEM_NAMES]]

def tuple_to_str(tp):
    return ';'.join([str(v) for v in tp])

def str_to_tuple(s):
    return tuple([int(v) for v in s.split(';')])

class Tilemap():
    def __init__(self, total_level, cur_level):
        self.map_image = self.init_map_image()
        self.total_level = total_level
        self.cur_level = cur_level

        # Map
        self.game_map = load_dict_map_json('assets/map/', self.total_level)
        self.game_map_entity = load_dict_entity('assets/map/', self.total_level)
        self.cur_map = self.game_map[self.cur_level]
        self.cur_entity = self.game_map_entity[self.cur_level]
        self.tile_size = self.map_image[1].get_width()

        # Chunk
        self.chunk_x, self.chunk_y = [0, 15], [0, 26]
        self.tile_chunk = self.init_tile_chunk()
        self.entity_chunk = self.init_entity_chunk()

        # Tile and entity
        self.tiles = self.init_tiles()
        self.entities = self.init_entities(CATEGORIES)

    def init_map_image(self):
        map_image = {}
        for index, file_name in enumerate(FILE_NAMES):
            img_path = 'assets/images/pillar/' + file_name
            map_image[index] = load_image(img_path)
        return map_image

    def init_tile_chunk(self):
        tile_chunk = []
        min_row = self.chunk_x[0]
        max_row = self.chunk_x[1]
        min_col = self.chunk_y[0]
        max_col = self.chunk_y[1]
        for row in range(min_row, max_row):
            rows = []
            for col in range(min_col, max_col):
                rows.append(self.cur_map[row][col])
            tile_chunk.append(rows)
        return tile_chunk

    def init_entity_chunk (self):
        entity_chuck = []
        min_row = self.chunk_x[0] * self.tile_size
        max_row = self.chunk_x[1] * self.tile_size
        min_col = self.chunk_y[0] * self.tile_size
        max_col = self.chunk_y[1] * self.tile_size
        for entity in self.cur_entity:
            x = entity["x"] - entity["originX"]
            y = entity["y"] - entity["originY"]
            if x > min_col and x < max_col and y > min_row and y < max_row:
                entity_chuck.append(entity)
        return entity_chuck

    def init_tiles(self):
        tiles = []
        min_row = self.chunk_x[0]
        min_col = self.chunk_y[0]
        for row, data_x in enumerate(self.tile_chunk):
            for col, index in enumerate(data_x):
                if index != -1:
                    tile = Tile((col + min_col) * self.tile_size, (row + min_row)* self.tile_size, index, self.map_image[index])
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

    def change_chunk(self, player_x, player_y):
        # if player_y > self.chunk_x[1] * self.tile_size:
        #     print(player_x, (self.chunk_x[1] - 1) * self.tile_size)
        #     self.chunk_x[0] = self.chunk_x[1]
        #     self.chunk_x[1] += 15
        #     self.move_chunk()
        #     return True

        if player_x <= (self.chunk_y[0])* self.tile_size:
            self.chunk_y[0] = 0
            self.chunk_y[1] = 26
            self.move_chunk()
            return True

        if player_x >= (self.chunk_y[1] -2 )* self.tile_size:
            self.chunk_y[0] = self.chunk_y[1] - 4
            self.chunk_y[1] += 24
            if self.chunk_y[1] > 24 *2:
                self.chunk_y[1] = 24* 2
            self.move_chunk()
            return True
        return False

    def move_chunk(self):
        self.tile_chunk = self.init_tile_chunk()
        self.entity_chunk = self.init_entity_chunk()
        self.tiles = self.init_tiles()
        self.entities = self.init_entities(CATEGORIES)

    def change_level(self, level):
        self.cur_level = level
        self.cur_map = self.game_map[self.cur_level]
        self.cur_entity = self.game_map_entity[self.cur_level]
        self.move_chunk()
    
