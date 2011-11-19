import pygame

from pygame.locals import *
from globals import *

class ImageController(object):
    def __init__(self):
        self.init_images()

    def load_image(self, filename):
        img = pygame.image.load(filename).convert()
        img.set_colorkey(TRANSPARENT)

        return img

    def init_images(self):
        self.dragon = self.load_image("resources/Dragon.gif")
        self.boss = self.load_image("resources/Boss.gif")
        self.boss_hit = self.load_image("resources/Boss_Hit.gif")
        self.fireball = self.load_image("resources/Fireball.gif")
        self.demon = self.load_image("resources/Demon.gif")
        self.baby = self.load_image("resources/Baby.gif")
        self.heart = self.load_image("resources/Heart.gif")

    def get_images(self):
        return self.dragon, self.boss, self.boss_hit, self.fireball, self.demon, self.baby, self.heart
