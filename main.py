import pygame, sys

from pygame.locals import *
from color import *
from game import World
from player import Player

pygame.init()
pygame.font.init()
pygame.mixer.init()
pygame.mixer.pre_init(44100, -16, 2, 512)

WIDTH, HEIGHT = 768, 432
SCALE = 2
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
DIS = pygame.Surface((WIDTH //SCALE, HEIGHT //SCALE))

CLOCK = pygame.time.Clock()
FPS = 60

# Music
pygame.mixer.music.load('assets/music/music.wav')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(loops = -1)

def quit():
    pygame.quit()
    sys.exit()

def draw(world, player):
    WIN.fill(WHITE)
    DIS.fill(WHITE)
    world.draw(DIS)
    player.draw(DIS)
    # player.draw_rect(DIS)
    
def main():

    player = Player(180, 200)
    world = World(player)

    run = True
    while run: 
        CLOCK.tick(FPS)

        for event in pygame.event.get():
            if event.type == QUIT:
                quit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    quit()

                if event.key == K_r:
                    world.reset(world.level)

        world.collision_test()
        player.handle_key_pressed()
        
        if world.fade == 2:
            timer = 40
            world.fade -= 1
            while timer > 0:
                screenshoot = pygame.transform.scale(DIS, (WIDTH, HEIGHT))
                timer -= 1
                black = pygame.Surface((WIDTH, HEIGHT))
                black.set_alpha(255- 255/40 *timer)
                screenshoot.blit(black, (0, 0))
                WIN.blit(screenshoot, (0, 0))
                pygame.display.update()
                CLOCK.tick(FPS)
            world.reset(world.level + 1)
        
        if world.tilemap.change_chunk(player.rect.x, player.rect.y):
            world.tiles = world.tilemap.tiles
            world.entities = world.tilemap.entities
            origin_x, origin_y = -WIDTH, 0

        draw(world, player)
                
        surf = pygame.transform.scale(DIS, (WIDTH, HEIGHT))
        
        WIN.blit(surf, (0, 0))
        pygame.display.update()

if __name__ == "__main__":
    main()
