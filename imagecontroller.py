import pygame

from pygame.locals import *
from globals import *

#image IDs
dragon_img = 'dragon'
boss_img = 'boss'
boss_hit_img = 'boss_hit'
fireball_img = 'fireball'
demon_img = 'demon'
baby_img = 'baby'
heart_img = 'heart'

class ImageController(object):
    def __init__(self):
        self.images = {}
        self.init_images()

    def load_image(self, filename):
        img = pygame.image.load(filename).convert()
        img.set_colorkey(TRANSPARENT)

        return img

    def init_images(self):
        self.images[dragon_img] = self.load_image("resources/Dragon.gif")
        self.images[boss_img] = self.load_image("resources/Boss.gif")
        self.images[boss_hit_img] = self.load_image("resources/Boss_Hit.gif")
        self.images[fireball_img] = self.load_image("resources/Fireball.gif")
        self.images[demon_img] = self.load_image("resources/Demon.gif")
        self.images[baby_img] = self.load_image("resources/Baby.gif")
        self.images[heart_img] = self.load_image("resources/Heart.gif")

    def get_images(self):
        return self.images[dragon_img], self.images[boss_img], self.images[boss_hit_img], self.images[fireball_img], self.images[demon_img], self.images[baby_img], self.images[heart_img]

    def get_image(self, id):
        return self.images[id]

    def get_background(self):
        return self.load_image("resources/Background800x480.bmp").convert()
