from random import random 
import pygame, os

from color import *

pygame.font.init()
pygame.mixer.init()
pygame.mixer.pre_init(44100, -16, 2, 512)


FILE_NAMES = ['dirt', 'grass', 'chair_pillar', 'ladder', 'pillar_0', 'pillar_1', 'table_pillar']
BOOK_NAMES = ['book_0', 'book_1', 'book_2', 'book_3']
ITEM_NAMES = ['bottle', 'shell', 'table']
LEVEL_NAMES = ['level_1', 'level_2', 'level_3', 'level_4', 'level_5', 'level_6']


MAP_IMAGE = {}
BOOK_IMAGE = {}
ITEM_IMAGE = {}
GAME_MAP = {}

def load_image(path):
    path = path + '.png'
    img = pygame.image.load(path)
    return img

def load_map(path):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map

for index, file_name in enumerate(FILE_NAMES):
    index += 1
    if index == 1 or index == 2:
        img_path = 'assets/images/' + file_name
    if index >= 3 and index <= 7:
        img_path = 'assets/images/pillar/' + file_name
    MAP_IMAGE[index] = load_image(img_path)

for index, book_name in enumerate(BOOK_NAMES):
    img_path = 'assets/images/book/' + book_name
    BOOK_IMAGE[index] = load_image(img_path)
    index += 1

for index, item_name in enumerate(ITEM_NAMES):
    img_path = 'assets/images/item/' + item_name
    ITEM_IMAGE[index] = load_image(img_path)
    index += 1

for index, level_name in enumerate(LEVEL_NAMES):
    index += 1
    map_path = 'assets/map/' + level_name
    GAME_MAP[index]  = load_map(map_path)
    
# Size
TILE_SIZE = MAP_IMAGE[1].get_width()
BOOK_2_WIDTH, BOOK_2_HEIGHT = 14, 5

# Pos
GROUND_Y = 192
TABLE_Y = GROUND_Y - 6
SHELL_Y = GROUND_Y - 16

# Font
TEXT_FONT = pygame.font.SysFont("comicsans", 9)

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
        self.tile_rects = self.init_tiles()
        self.books = self.init_books()
        self.items = self.init_items()
        self.texts = self.init_texts()
        self.tutorial_texts = self.init_tutorial_texts()
        self.fade = -1

    def init_tiles(self):
        tile_rects = []
        for row, data in enumerate(self.cur_map):
            for col, tile in enumerate(data):
                if tile != '0':
                    rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    tile_rects.append((int(tile), rect))
        return tile_rects

    def init_books(self):
        books = []
        if self.level == 1:
            book = Book(100, GROUND_Y, 1)
            books.append(book)

        elif self.level == 2:
            book_0 = Book(250, GROUND_Y, 0)
            book_1 = Book(70, GROUND_Y, 1)
            book_2 = Book(165, GROUND_Y, 2)
            books.extend([book_1, book_0, book_2])

        elif self.level == 3:
            book_1 = Book(50, GROUND_Y, 1)
            book_0 = Book(153, GROUND_Y - 6, 0)
            book_21 = Book(350 - BOOK_2_WIDTH,  GROUND_Y, 2)
            book_22 = Book(350 - BOOK_2_WIDTH, GROUND_Y - BOOK_2_HEIGHT, 2)
            book_24 = Book(165, GROUND_Y, 2)
            books.extend([book_1, book_0, book_21, book_22, book_24])
            for i in range(2):
                book_0 = Book(250 + i*15, GROUND_Y, 0)
                books.append(book_0)

        elif self.level == 4:
            book_1 = Book(350, GROUND_Y, 1)
            book_0 = Book(320,GROUND_Y, 0)
            book_01 = Book(90, GROUND_Y, 0)
            book_02 = Book(75, GROUND_Y, 0)
            book_03 = Book(60, GROUND_Y, 0)
            book_2 = Book(155, GROUND_Y, 2)
            book_21 = Book(34, GROUND_Y, 2)
            book_22 = Book(34, GROUND_Y - 5, 2)
            book_23 = Book(126, GROUND_Y, 2)
            books.extend([book_1, book_0, book_01, book_02, book_03, book_2, book_21, book_22, book_23])

        elif self.level == 5: 
            book_1 = Book(350, GROUND_Y, 1)
            book_0 = Book(200,GROUND_Y, 0)
            book_01 = Book(90, GROUND_Y, 0)
            book_02 = Book(75, GROUND_Y, 0)
            book_03 = Book(60, GROUND_Y, 0)
            book_04 = Book(252, SHELL_Y, 0)
            book_05 = Book(105, GROUND_Y, 0)
            book_2 = Book(155, GROUND_Y, 2)
            book_21 = Book(34, GROUND_Y, 2)
            book_22 = Book(34, GROUND_Y - 5, 2)
            book_23 = Book(126, GROUND_Y, 2)
            book_24 = Book(236, GROUND_Y, 2)
            book_25 = Book(236, GROUND_Y -5, 2)
            books.extend([book_1, book_0, book_01, book_02, book_03, book_04, book_05, book_2, book_21, book_22, book_23, book_24, book_25])

        # elif self.level == 6:
            

        elif self.level == 6:
            book_0 = Book(160, 112, 1)
            books.append(book_0)


            
        return books

    def init_items(self):
        items = []
        if self.level == 1:
            item = Item(250, GROUND_Y, 0)
            items.append(item)

        elif self.level == 2:
            item_0 = Item(154, TABLE_Y, 0)
            item_2 = Item(150, GROUND_Y, 2)
            items.extend([item_0, item_2])

        elif self.level == 3:
            item_0 = Item(353, SHELL_Y, 0)
            item_1 = Item(350, GROUND_Y, 1)
            item_2 = Item(150, GROUND_Y, 2)
            items.extend([item_0, item_1, item_2])

        elif self.level == 4:
            item_0 = Item(23, SHELL_Y, 0)
            item_1 = Item(20, GROUND_Y, 1)
            item_2 = Item(140, GROUND_Y, 2)
            items.extend([item_0, item_1, item_2])

        elif self.level == 5:
            item_0 = Item(23, SHELL_Y, 0)
            item_1 = Item(20, GROUND_Y, 1)
            item_11 = Item(250, GROUND_Y, 1)
            item_2 = Item(140, GROUND_Y, 2)
            items.extend([item_0, item_1, item_11, item_2])

        # elif self.level == 6:

        elif self.level == 6:
            pass

        return items

    def init_texts(self):
        texts = []
        text_1 = "Dear Boss Baby,"
        text_2 = "I don't usually write very much but I know that memos are very important things"
        text_3 = "Even though never went to business school, I did learn to share in kindergarten."
        text_31 = "And if there isn't enough love for the two of us, then I will give you all of mine."
        text_4 = "I would like to offer you a job. It will be hard-work and there will be now pay"
        text_41 = "But the good news is that you will never be fired"
        text_5 = "And I promise you this. Every morning when you wake up, I will be there"
        text_51 = "Every night at dinner. I will be there"
        text_52 = "Every birthday party, every christmas morning I will be there"
        text_6 = "Year after year, after year"
        text_61 = "We will grow old together and you and I will always be brother. Always"
        text_7 = "Love, Timmy"
        text_71 = "Thanks for playing"


        if self.level == 1:
            texts.append(text_1)
        elif self.level == 2:
            texts.extend([text_1, text_2])
        elif self.level == 3:
            texts.extend([text_1, text_2, text_3, text_31])
        elif self.level == 4:
            texts.extend([text_1, text_2, text_3, text_31, text_4, text_41])
        elif self.level == 5:
            texts.extend([text_1, text_2, text_3, text_31, text_4, text_41, text_5, text_51, text_52, text_6, text_61])
        elif self.level == 6:
            texts.extend([text_7, text_71])
        return texts

    def init_tutorial_texts(self):
        texts = []
        text_1 = ["Use AD or arrow keys to move", (125, 150), True]
        text_2 = ["Drink bottle to turn to boss baby", (190, 150), False]
        text_3 = ["Read memo", (80, 150), False]
        text_4 = ["J/X to pick up book", (210, 150), True]
        text_5 = ["J/X to place book", (130, 150), False]
        text_6 = ["R to reset level", (150, 150), True]
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
        for index, text in enumerate(self.texts):
            text = TEXT_FONT.render(text, 2, PURPLE_BLACK)
            dis.blit(text, (20, 20 + 12*index))
        self.draw_tutorial(dis)

    def draw_tutorial(self, dis):
        if self.level == 1:
            text_0 = self.tutorial_texts[0]
            text_1 = self.tutorial_texts[1]
            text_2 = self.tutorial_texts[2]
            if text_0[2]:
                tutorial_text_0 = TEXT_FONT.render(text_0[0], 2, PURPLE_BLACK)
                dis.blit(tutorial_text_0, text_0[1])
            if text_1[2]:
                tutorial_text_1 = TEXT_FONT.render(text_1[0], 2, PURPLE_BLACK)
                dis.blit(tutorial_text_1, text_1[1])
            if text_2[2]:
                tutorial_text_2 = TEXT_FONT.render(text_2[0], 2, PURPLE_BLACK)
                dis.blit(tutorial_text_2, text_2[1])
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
                tutorial_text_3 = TEXT_FONT.render(text_3[0], 2, PURPLE_BLACK)
                dis.blit(tutorial_text_3, text_3[1])
            if text_4[2]:
                tutorial_text_4 = TEXT_FONT.render(text_4[0], 2, PURPLE_BLACK)
                dis.blit(tutorial_text_4, text_4[1])
            if self.player.book != None:
                text_3[2] = False
                text_4[2] = True
            if self.player.book == None and not text_3[2]:
                text_4[2] = False

        if self.level == 3:
            text_5 = self.tutorial_texts[5]
            if text_5[2]:
                tutorial_text_5 = TEXT_FONT.render(text_5[0], 2, PURPLE_BLACK)
                dis.blit(tutorial_text_5, text_5[1])

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
                crawl_book_y = rect.y + 7
                walk_y = rect.y + 10
                if item.num == 2 :
                    crawl_y = rect.y + 5
                    crawl_book_y = rect.y + 10
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
        if len(self.items) > 0:
            if self.items[0].collide(rect):
                bottle_fx.play()
                self.player.change_action("crawl", "walk")
                self.items.remove(self.items[0])

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
        self.player.reset(180, 184)
        self.level = level
        self.cur_map = GAME_MAP[self.level]
        self.tile_rects = self.init_tiles()
        self.books = self.init_books()
        self.items = self.init_items()
        self.texts = self.init_texts()
        self.fade = -1

class Book:
    def __init__(self, x, y, num):
        # 0 is book of bottle, 1 is book of love
        self.num = num
        self.img = BOOK_IMAGE[num]
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y - self.img.get_height()
        self.show = self.init_show()

    def init_show(self):
        if self.num >= 2:
            return False
        return True

    def draw(self, dis):
        if self.show:
            dis.blit(self.img, (self.rect.x, self.rect.y))

    def draw_rect(self, dis):
        pygame.draw.rect(dis, BLACK, self.rect, 1)

    def collide(self, rect):
        if self.rect.colliderect(rect):
            return True
        return False

class Item:
    def __init__(self, x, y, num):
        # 0 is bottle, 1 is shell, 2 is table
        self.num = num
        self.img = ITEM_IMAGE[num]
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y - self.img.get_height()

    def draw(self, dis):
        dis.blit(self.img, (self.rect.x, self.rect.y))

    def draw_rect(self, dis):
        pygame.draw.rect(dis, BLACK, self.rect, 1)

    def collide(self, rect):
        if self.rect.colliderect(rect):
                return True
        return False
