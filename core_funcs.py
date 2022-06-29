import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PINK = (255, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)


# read File
def read_f(path):
    f = open(path, 'r')
    data = f.read()
    f.close()
    return data

def write_f(path, data):
    f = open(path, 'w')
    f.write(data)
    f.close()

def swap_color(img, old_color, new_color):
    img.set_colorkey(old_color)
    dis = img.copy()
    dis.fill(new_color)
    dis.blit(img, (0, 0))
    return dis

# Cut the image
def clip(dis, x, y, width, height):
    copy_dis = dis.copy()
    clip_rect = pygame.Rect(x, y, width, height)
    copy_dis.set_clip(clip_rect)
    image = dis.subsurface(copy_dis.get_clip())
    return image.copy()

# Return corners of a rect
def rect_corners(points):
    point_1 = points[0]
    point_2 = points[1]
    out_1 = [min(point_1[0], point_2[0]), min(point_1[1], point_2[1])]
    out_2 = [max(point_1[0], point_2[0]), max(point_1[1], point_2[1])]
    return [out_1, out_2]

def corner_rect(points):
    points = rect_corners(points)
    x = points[0][0]
    y = points[0][1]
    width = points[1][0] - points[0][0]
    height = points[1][1] - points[0][1]
    rect = pygame.Rect(x, y, width, height)
    return rect

def points_between_2d(points):
    points = rect_corners(points)
    width = points[1][0] - points[0][0] + 1
    height = points[1][1] - points[0][1] + 1
    point_list = []
    for y in range(height):
        for x in range(width):
            point_list.append([points[0][0] + x, points[0][1] + y])
    return point_list

def angle_to(points):
    pass

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