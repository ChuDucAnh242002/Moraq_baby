import pygame, sys, json

from pygame.locals import *
from color import *
from game import World
from player import Player

pygame.init()
pygame.font.init()
pygame.mixer.init()
pygame.mixer.pre_init(44100, -16, 2, 512)

WIN_SIZE = (768, 432)
WIDTH, HEIGHT = 384 ,216
WIN = pygame.display.set_mode(WIN_SIZE)
DIS = pygame.Surface((WIDTH, HEIGHT))

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
                screenshoot = pygame.transform.scale(DIS, (WIN_SIZE[0], WIN_SIZE[1]))
                timer -= 1
                black = pygame.Surface((WIN_SIZE[0], WIN_SIZE[1]))
                black.set_alpha(255- 255/40 *timer)
                screenshoot.blit(black, (0, 0))
                WIN.blit(screenshoot, (0, 0))
                pygame.display.update()
                CLOCK.tick(FPS)
            world.reset(world.level + 1)

        draw(world, player)
                
        surf = pygame.transform.scale(DIS, (WIN_SIZE[0], WIN_SIZE[1]))
        WIN.blit(surf, (0, 0))
        pygame.display.update()

if __name__ == "__main__":
    main()
