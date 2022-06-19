import pygame

from color import BLACK

pygame.mixer.init()
pygame.mixer.pre_init(44100, -16, 2, 512)

global animation_frames
animation_frames = {}

def load_animation(path, frame_durations):
    global animation_frames
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    for n, frame in enumerate(frame_durations):
        animation_frame_id = animation_name + '_' + str(n)
        img_loc = path + '/' + animation_frame_id + '.png'
        # player_animations/idle/idle_0.png
        animation_image = pygame.image.load(img_loc)
        animation_image.set_colorkey((255,255,255))
        animation_frames[animation_frame_id] = animation_image.copy()
        for _ in range(frame):
            animation_frame_data.append(animation_frame_id)
    return animation_frame_data

animation_database = {}

animation_database['crawl'] = load_animation('assets/images/crawl', [7, 7, 7, 7])
animation_database['crawl_book'] = load_animation('assets/images/crawl_book', [7, 7, 7, 7])
animation_database['walk'] = load_animation('assets/images/walk', [7, 7, 7])
animation_database['idle'] = load_animation('assets/images/idle', [1, 1, 1])

class Player: 
    def __init__(self, x, y):
        # base img
        self.img = animation_frames['idle_0']
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.crawl= True
        self.crawl_book = False
        self.move = False
        self.jumped = False
        self.movement = [0, 0]
        self.frame = 0
        self.action = 'idle'
        self.flip = True
        self.in_air = True
        self.book = None

    def draw(self, dis):
        if self.action == 'crawl' or self.action == 'walk' or self.action == 'crawl_book':
            self.frame += 1
            if self.frame >= len(animation_database[self.action]):
                self.frame = 0
            img_id = animation_database[self.action][self.frame]
            img = animation_frames[img_id] 
            self.img = pygame.transform.flip(img, self.flip, False)
        self.rect.width = self.img.get_width()
        self.rect.height = self.img.get_height()
        dis.blit(self.img, (self.rect.x, self.rect.y))
        pygame.draw.rect(dis, BLACK, self.rect, 1)

    def handle_key_pressed(self):
        dx = 0
        dy = 0

        self.vel_y += 0.5
        if self.vel_y > 2:
            self.vel_y = 2
        dy += self.vel_y

        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            if self.crawl_book: 
                self.action = 'crawl_book'
            if self.crawl:
                self.action = 'crawl'
            if self.move:
                self.action = 'walk'
            self.flip = True
            dx += 1

        if keys[pygame.K_a]:
            if self.crawl_book: 
                self.action = 'crawl_book'
            if self.crawl:
                self.action = 'crawl'
            if self.move:
                self.action = 'walk'

            self.flip = False
            dx -= 1
                
        if self.move:
            if keys[pygame.K_w] and self.jumped == False and not self.in_air:
                self.vel_y = -2
                self.jumped = True
            if keys[pygame.K_w] == False:
                self.jumped = False

        if dx == 0:
            if self.crawl:
                img = animation_frames['idle_0']
                img = pygame.transform.scale(img, (img.get_width(), img.get_height()))
                self.img = pygame.transform.flip(img, self.flip, False)

            elif self.move:
                img = animation_frames['idle_1']
                img = pygame.transform.scale(img, (img.get_width(), img.get_height()))
                self.img = pygame.transform.flip(img, self.flip, False)

            elif self.crawl_book:
                img = animation_frames['idle_2']
                img = pygame.transform.scale(img, (img.get_width(), img.get_height()))
                self.img = pygame.transform.flip(img, self.flip, False)
            self.action = 'idle'
            self.frame = 0

        self.movement = [dx, dy]

    def pick_up(self, book):
        keys = pygame.key.get_pressed()
        if self.book == None:
            if keys[pygame.K_j] and self.crawl:
                self.book = book
                self.crawl = False
                self.crawl_book = True
                return True
        return False

    def put_down(self):
        if self.book != None:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_j] and self.crawl_book:
                self.book = None
                self.crawl = True
                self.crawl_book = False
                return True
        return False

    def reset(self, x, y):
        self.img = animation_frames['idle_0']
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.crawl= True
        self.crawl_book = False
        self.move = False
        self.jumped = False
        self.movement = [0, 0]
        self.frame = 0
        self.action = 'idle'
        self.flip = True
        self.in_air = True
        self.book = None