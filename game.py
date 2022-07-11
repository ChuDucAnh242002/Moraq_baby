import pygame

from core_funcs import *
from color import *
from text import Font
from tilemap import Tilemap

pygame.font.init()
pygame.mixer.init()
pygame.mixer.pre_init(44100, -16, 2, 512)

TOTAL_LEVEL = 8

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
        self.level = 8
        self.tilemap = Tilemap(TOTAL_LEVEL, self.level)
        self.tiles = self.tilemap.tiles
        self.entities = self.tilemap.entities
        self.texts = self.init_texts()
        self.tutorial_texts = self.init_tutorial_texts()
        self.fade = -1

        # Add new font
        self.font = Font('assets/font/small_font.png', PURPLE_BLACK)

    def init_texts(self):
        text_1 = "Dear Boss Baby,\n"
        text_2 = text_1 + "I don't usually write very much but I know that memos are very important things.\n"
        text_3 = text_2 + "Even though I never went to business school, I did learn to share in kindergarten.\nAnd if there isn't enough love for the two of us, then I will give you all of mine.\n"
        text_4 = text_3 + "I would like to offer you a job. It will be hard-work and there will be no pay.\nBut the good news is that you will never be fired.\n"
        text_5 = text_4 + "And I promise you this.\nEvery morning when you wake up, I will be there.\nEvery night at dinner, I will be there.\nEvery birthday party, every christmas morning I will be there.\n"
        text_6 = text_5 + "Year after year, after year.\nWe will grow old together and you and I will always be brother.\nAlways!"
        text_7 = "Love, Timmy\nThanks for playing"

        texts = [text_1, text_2, text_3, text_4, text_5, text_6, text_7]
        if self.level <= 7:
            text = texts[self.level - 1]
            return text
        else: return None

    def init_tutorial_texts(self):
        texts = []
        text_1 = ["Use AD or arrow keys to move", (130, 176), True]
        text_2 = ["Drink bottle to turn to boss baby", (190, 176), False]
        text_3 = ["Read memo", (85, 176), False]
        text_4 = ["J/X to pick up book", (225, 176), True]
        text_5 = ["J/X to place book", (125, 176), False]
        text_6 = ["R to reset level", (160, 176), True]
        text_7 = ["Bonus level", (305, 176), True]
        texts.extend([text_1, text_2, text_3, text_4, text_5, text_6, text_7])
        return texts

    def draw(self, dis):
        for tile in self.tiles:
            tile.draw(dis)
        for list_entity in self.entities.values():
            for entity in list_entity:
                entity.draw(dis)
        if self.texts != None:
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
        for tile in self.tiles:
            if rect.colliderect(tile.rect) and (tile.name == 0 or tile.name == 1):
                hit_list.append(tile.rect)
        return hit_list

    def collision_test(self):
        rect = self.player.rect
        movement = self.player.movement

        rect.x += movement[0]
        hit_list = self.hit(rect)
        
        for tile in hit_list:
            self.re_pos(tile)

        for entity in self.entities["items"]:
            if entity.name == "bottle": continue
            if entity.collide(rect):
                crawl_y = rect.y + 2
                crawl_book_y = rect.y + 5
                walk_y = rect.y + 10
                if entity.name == "table" :
                    crawl_y = rect.y + 5
                    crawl_book_y = rect.y + 8
                    walk_y = rect.y + 13
                if (self.player.crawl and crawl_y > entity.rect.y) or (self.player.crawl_book and crawl_book_y > entity.rect.y) or (self.player.move and walk_y > entity.rect.y):
                    self.re_pos(entity.rect)

        # vertical
        rect.y += movement[1]
        hit_list = self.hit(rect)
        for tile in hit_list:
            self.re_pos_y(tile)
                

        for entity in self.entities["items"]:
            if (entity.name == "table" or entity.name == "shell") and entity.collide(rect):
                self.re_pos_y(entity.rect)

        for entity in self.entities["books"]:
            if entity.name == "book_2" and entity.collide(rect):
                if entity.show:
                    self.re_pos_y(entity.rect)

        self.collide_book(rect)
        self.collide_item(rect)


        



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

    def collide_item(self, rect):
        for entity in self.entities["items"]:
            if entity.name == "bottle" and entity.collide(rect):
                bottle_fx.play()
                self.player.change_action("crawl", "walk")
                self.entities["items"].remove(entity)

    def collide_book(self, rect):
        for entity in self.entities["books"]:
            if entity.name == "book_0" and entity.collide(rect):
                if self.player.pick_up(entity):
                    pick_up_fx.play()
                    self.entities["books"].remove(entity)
            if entity.name == "book_1" and entity.collide(rect) and self.player.move:
                love_book_fx.play()
                self.fade = 2
            if entity.name == "book_2" and entity.collide(rect):
                if self.player.put_down():
                    put_down_fx.play()
                    entity.show = True

    def reset(self, level):
        self.player.reset(180, 200)
        self.level = level
        self.tilemap.change_level(level)
        self.tiles = self.tilemap.tiles
        self.entities = self.tilemap.entities
        self.texts = self.init_texts()
        self.tutorial_texts = self.init_tutorial_texts()
        self.fade = -1
