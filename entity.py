import pygame

from core_funcs import *

BOOK_NAMES = ['book_0', 'book_1', 'book_2']
ITEM_NAMES = ['bottle', 'shell', 'table']

BOOK_IMAGE = load_dict_image('assets/images/book/', BOOK_NAMES)
ITEM_IMAGE = load_dict_image('assets/images/item/', ITEM_NAMES)

class Entity:
    def __init__(self, x, y, name, img):
        self.name = name
        self.img = img
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        # self.show = True

    def draw(self, dis):
        dis.blit(self.img, (self.rect.x, self.rect.y))

    def draw_rect(self, dis):
        pygame.draw.rect(dis, BLACK, self.rect, 1)

    def collide(self, rect):
        if self.rect.colliderect(rect):
            return True
        return False

class Tile(Entity):
    def __init__(self, x, y, index, img):
        super().__init__(x, y, index, img)

class Book(Entity):
    def __init__(self, x, y, name):
        # 0 is book of bottle, 1 is book of love
        super().__init__(x, y, name, BOOK_IMAGE[name])
        self.show = self.init_show()

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
        super().__init__(x, y, name, ITEM_IMAGE[name])
