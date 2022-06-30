import pygame

from core_funcs import *


class Entity:
    def __init__(self, x, y, name, img):
        self.name = name
        self.img = img
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
