import pygame

from core_funcs import *

class Animation:
    def __init__(self):
        self.animation_frames = {}
        self.animation_database = {}
        self.animation_data = load_json_data('assets/animation/animation')
        self.init_data()

    def add_action(self, action, frame_durations):
        path = 'assets/images/' + action
        self.animation_database[action] = self.add_frame(path, frame_durations)

    def add_frame(self, path, frame_durations):
        animation_name = path.split('/')[-1]
        animation_frame_data = []
        for n, frame in enumerate(frame_durations):
            animation_frame_id = animation_name + '_' + str(n)
            img_loc = path + '/' + animation_frame_id + '.png'
            # player_animations/idle/idle_0.png
            animation_image = pygame.image.load(img_loc)
            animation_image.set_colorkey((255,255,255))
            self.animation_frames[animation_frame_id] = animation_image.copy()
            for _ in range(frame):
                animation_frame_data.append(animation_frame_id)
        return animation_frame_data

    def init_data(self):
        for animation in self.animation_data["animations"]:
            self.add_action(animation["action"], animation["frame_durations"])