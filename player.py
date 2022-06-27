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
        self.movement = [0, 0]
        self.frame = 0
        self.action = 'idle'
        self.flip = True
        self.book = None

    def draw(self, dis):
        if self.action != 'idle':
            self.frame += 1
            if self.frame >= len(animation_database[self.action]):
                self.frame = 0
            img_id = animation_database[self.action][self.frame]
            self.img = animation_frames[img_id] 
        self.img = pygame.transform.flip(self.img, self.flip, False)
        self.rect.width = self.img.get_width()
        self.rect.height = self.img.get_height()
        dis.blit(self.img, (self.rect.x, self.rect.y))
        
    def draw_rect(self, dis):
        pygame.draw.rect(dis, BLACK, self.rect, 1)

    def handle_key_pressed(self):
        dx = 0
        dy = 0

        self.vel_y += 0.5
        if self.vel_y > 3:
            self.vel_y = 3
        dy += self.vel_y

        keys = pygame.key.get_pressed()
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.check_action()
            self.flip = True
            dx += 1

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.check_action()
            self.flip = False
            dx -= 1
                
        if dx == 0:
            self.change_idle_img()
            self.action = 'idle'
            self.frame = 0

        self.movement = [dx, dy]

    def pick_up(self, book):
        if self.book == None:
            keys = pygame.key.get_pressed()
            if (keys[pygame.K_j] or keys[pygame.K_x]) and self.crawl:
                self.book = book
                self.change_action("crawl", "crawl_book")
                return True
        return False

    def put_down(self):
        if self.book != None:
            keys = pygame.key.get_pressed()
            if (keys[pygame.K_j] or keys[pygame.K_x]) and self.crawl_book:
                self.book = None
                self.change_action("crawl_book", "crawl")
                return True
        return False

    def change_action(self, old_action, new_action):
        if old_action == "crawl": self.crawl = False
        elif old_action == "crawl_book": self.crawl_book = False
        elif old_action == "walk": self.move = False
        if new_action == "crawl": self.crawl = True
        elif new_action == "crawl_book": self.crawl_book = True
        elif new_action == "walk": self.move = True
        
        if new_action == "walk" : 
            self.rect.x += 3
            self.rect.y -= 11
        if new_action == "crawl_book":
            self.rect.y -= 6

    def check_action(self):
        if self.crawl_book:
            self.action = 'crawl_book'
        if self.crawl:
            self.action = 'crawl'
        if self.move:
            self.action = 'walk'

    def change_idle_img(self):
        if self.crawl:
            self.img = animation_frames['idle_0']
        elif self.move:
            self.img = animation_frames['idle_1']
        elif self.crawl_book:
            self.img = animation_frames['idle_2']

    def reset(self, x, y):
        self.img = animation_frames['idle_0']
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.crawl= True
        self.crawl_book = False
        self.move = False
        self.movement = [0, 0]
        self.frame = 0
        self.action = 'idle'
        self.flip = True
        self.book = None