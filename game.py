import pygame

from core_funcs import *
from color import *
from text import Font

pygame.font.init()
pygame.mixer.init()
pygame.mixer.pre_init(44100, -16, 2, 512)

FILE_NAMES = ['grass', 'dirt', 'chair_pillar', 'ladder', 'pillar_0', 'pillar_1', 'table_pillar']
BOOK_NAMES = ['book_0', 'book_1', 'book_2']
ITEM_NAMES = ['bottle', 'shell', 'table']

MAP_IMAGE = {}

for index, file_name in enumerate(FILE_NAMES):
    if index == 0 or index == 1:
        img_path = 'assets/images/' + file_name
    if index >= 2 and index <= 6:
        img_path = 'assets/images/pillar/' + file_name
    MAP_IMAGE[index + 1] = load_image(img_path)

TOTAL_LEVEL = 7
BOOK_IMAGE = load_dict_image('assets/images/book/', BOOK_NAMES)
ITEM_IMAGE = load_dict_image('assets/images/item/', ITEM_NAMES)
GAME_MAP = load_dict_map_json('assets/map/', TOTAL_LEVEL)
GAME_MAP_ENTITY = load_dict_entity('assets/map/', TOTAL_LEVEL)
# Size
TILE_SIZE = MAP_IMAGE[1].get_width()
BOOK_2_WIDTH, BOOK_2_HEIGHT = 14, 5

# Pos
GROUND_Y = 192
TABLE_Y = GROUND_Y - 6
SHELL_Y = GROUND_Y - 16

# sfx
pick_up_fx = pygame.mixer.Sound('assets/sfx/pick_up.wav')
put_down_fx = pygame.mixer.Sound('assets/sfx/put_down.wav')
bottle_fx = pygame.mixer.Sound('assets/sfx/bottle.wav')
love_book_fx = pygame.mixer.Sound('assets/sfx/love_book.wav')

pick_up_fx.set_volume(0.1)
put_down_fx.set_volume(0.1)
bottle_fx.set_volume(0.1)
love_book_fx.set_volume(0.1)

class World:
    def __init__(self, player):
        self.player = player
        self.level = 1
        self.cur_map = GAME_MAP[self.level]
        self.cur_entity = GAME_MAP_ENTITY[self.level]
        self.tile_rects = self.init_tiles()
        self.books = self.init_books()
        self.items = self.init_items()
        self.texts = self.init_texts()
        self.tutorial_texts = self.init_tutorial_texts()
        self.fade = -1

        # Add new font
        self.font = Font('assets/font/small_font.png', PURPLE_BLACK)

    def init_tiles(self):
        tile_rects = []
        for row, data in enumerate(self.cur_map):
            for col, tile in enumerate(data):
                if tile != -1:
                    rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    tile_rects.append((tile + 1, rect))
        return tile_rects

    def init_books(self):
        books = []
        for entity in self.cur_entity:
            name = entity["name"]
            if name in BOOK_NAMES:
                x = entity["x"] - entity["originX"]
                y = entity["y"] - entity["originY"]
                book = Book(x, y, name)
                books.append(book)
        return books

    def init_items(self):
        items = []
        for entity in self.cur_entity:
            name = entity["name"]
            if name in ITEM_NAMES:
                x = entity["x"] - entity["originX"]
                y = entity["y"] - entity["originY"]
                item = Item(x, y, name)
                items.append(item)
        return items

    def init_texts(self):
        text_1 = "Dear Boss Baby,\n"
        text_2 = text_1 + "I don't usually write very much but I know that memos are very important things.\n"
        text_3 = text_2 + "Even though I never went to business school, I did learn to share in kindergarten.\nAnd if there isn't enough love for the two of us, then I will give you all of mine.\n"
        text_4 = text_3 + "I would like to offer you a job. It will be hard-work and there will be no pay.\nBut the good news is that you will never be fired.\n"
        text_5 = text_4 + "And I promise you this.\nEvery morning when you wake up, I will be there.\nEvery night at dinner, I will be there.\nEvery birthday party, every christmas morning I will be there.\n"
        text_6 = text_5 + "Year after year, after year.\nWe will grow old together and you and I will always be brother.\nAlways!"
        text_7 = "Love, Timmy\nThanks for playing"

        texts = [text_1, text_2, text_3, text_4, text_5, text_6, text_7]

        text = texts[self.level - 1]
        return text

    def init_tutorial_texts(self):
        texts = []
        text_1 = ["Use AD or arrow keys to move", (130, 176), True]
        text_2 = ["Drink bottle to turn to boss baby", (190, 176), False]
        text_3 = ["Read memo", (85, 176), False]
        text_4 = ["J/X to pick up book", (225, 176), True]
        text_5 = ["J/X to place book", (125, 176), False]
        text_6 = ["R to reset level", (160, 176), True]
        texts.extend([text_1, text_2, text_3, text_4, text_5, text_6])
        return texts

    def draw(self, dis):
        for tile in self.tile_rects:
            index = tile[0]
            dis.blit(MAP_IMAGE[index], (tile[1].x, tile[1].y))
        for book in self.books:
            book.draw(dis)
            # book.draw_rect(dis)
        for item in self.items:
            item.draw(dis)
            # item.draw_rect(dis)
        self.font.render_english(self.texts, dis, (20, 20))
        self.draw_tutorial(dis)

    def draw_tutorial(self, dis):
        if self.level == 1:
            text_0 = self.tutorial_texts[0]
            text_1 = self.tutorial_texts[1]
            text_2 = self.tutorial_texts[2]
            if text_0[2]:
                self.font.render_english(text_0[0], dis, text_0[1])
            if text_1[2]:
                self.font.render_english(text_1[0], dis, text_1[1])
            if text_2[2]:
                self.font.render_english(text_2[0], dis, text_2[1])
            
            movement = self.player.movement
            if movement[0] != 0:
                text_0[2] = False
                text_1[2] = True
            if self.player.move:
                text_1[2] = False
                text_2[2] = True

        if self.level == 2:
            text_3 = self.tutorial_texts[3]
            text_4 = self.tutorial_texts[4]
            if text_3[2]:
                self.font.render_english(text_3[0], dis, text_3[1])
            if text_4[2]:
                self.font.render_english(text_4[0], dis, text_4[1])
            if self.player.book != None:
                text_3[2] = False
                text_4[2] = True
            if self.player.book == None and not text_3[2]:
                text_4[2] = False

        if self.level == 3:
            text_5 = self.tutorial_texts[5]
            if text_5[2]:
                self.font.render_english(text_5[0], dis, text_5[1])

    def hit(self, rect):
        hit_list = []
        for tile in self.tile_rects:
            if rect.colliderect(tile[1]) and (tile[0] == 1 or tile[0] == 2):
                hit_list.append(tile[1])
        return hit_list

    def collision_test(self):
        rect = self.player.rect
        movement = self.player.movement

        rect.x += movement[0]
        hit_list = self.hit(rect)
        for tile in hit_list:
            self.re_pos(tile)
        for item in self.items:
            if item.num == 0 : continue
            if item.collide(rect):
                crawl_y = rect.y + 2
                crawl_book_y = rect.y + 5
                walk_y = rect.y + 10
                if item.num == 2 :
                    crawl_y = rect.y + 5
                    crawl_book_y = rect.y + 8
                    walk_y = rect.y + 13
                if (self.player.crawl and crawl_y > item.rect.y) or (self.player.crawl_book and crawl_book_y > item.rect.y) or (self.player.move and walk_y > item.rect.y):
                    self.re_pos(item.rect)

        rect.y += movement[1]
        hit_list = self.hit(rect)
        for tile in hit_list:
            self.re_pos_y(tile)

        for item in self.items:
            if item.num > 0 and item.collide(rect):
                self.re_pos_y(item.rect)
                
        for book in self.books:
            if book.num >= 2 and book.collide(rect) and book.show:
                self.re_pos_y(book.rect)

        self.collide_book()
        self.collide_item()

    def re_pos(self, entity):
        rect = self.player.rect
        movement = self.player.movement
        if movement[0] > 0:
            rect.right = entity.left
        elif movement[0] < 0:
            rect.left = entity.right

    def re_pos_y(self, entity):
        rect = self.player.rect
        movement = self.player.movement
        if movement[1] > 0:
            rect.bottom = entity.top
        elif movement[1] < 0:
            rect.top = entity.bottom

    def collide_item(self):
        rect = self.player.rect
        for item in self.items:
            if item.num == 0 and item.collide(rect):
                bottle_fx.play()
                self.player.change_action("crawl", "walk")
                self.items.remove(item)

    def collide_book(self):
        rect = self.player.rect
        for book in self.books:
            if book.num == 0 and book.collide(rect):
                if self.player.pick_up(book):
                    pick_up_fx.play()
                    self.books.remove(book)
            if book.num == 1 and book.collide(rect) and self.player.move:
                love_book_fx.play()
                self.fade = 2
            if book.num == 2 and book.collide(rect):
                if self.player.put_down():
                    put_down_fx.play()
                    book.show = True

    def reset(self, level):
        self.player.reset(180, 200)
        self.level = level
        self.cur_map = GAME_MAP[self.level]
        self.cur_entity = GAME_MAP_ENTITY[self.level]
        self.tile_rects = self.init_tiles()
        self.books = self.init_books()
        self.items = self.init_items()
        self.texts = self.init_texts()
        self.fade = -1

class Entity:
    def __init__(self, x, y, name):
        self.name = name
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, dis):
        dis.blit(self.img, (self.rect.x, self.rect.y))

    def draw_rect(self, dis):
        pygame.draw.rect(dis, BLACK, self.rect, 1)

    def collide(self, rect):
        if self.rect.colliderect(rect):
            return True
        return False

class Book(Entity):
    def __init__(self, x, y, name):
        # 0 is book of bottle, 1 is book of love
        self.img = BOOK_IMAGE[name]
        super().__init__(x, y, name)
        self.show = self.init_show()
        self.type, self.num = name.split("_")
        self.num = int(self.num)

    def init_show(self):
        if self.name == "book_2":
            return False
        return True

    def draw(self, dis):
        if self.show:
            super().draw(dis)

class Item(Entity):
    def __init__(self, x, y, name):
        # 0 is bottle, 1 is shell, 2 is table
        if name == "bottle": self.num = 0
        elif name == "shell": self.num = 1
        elif name == "table": self.num = 2
        self.img = ITEM_IMAGE[name]
        super().__init__(x, y, name)