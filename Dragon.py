import pygame
import sys
import time
import random
from pygame.locals import *

class Dragon(pygame.sprite.Sprite):
    def __init__(self, image, screen):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.screen = screen
        self.screen_size = screen.get_size()
        self.rect = self.image.get_rect()
        self.rect.topleft = (4, 200)
        self.step = 8
        self.timer = 0

    def move(self, key):
        rect = self.rect

        if key == K_UP:
            if rect.top > self.step:
                rect.top -= self.step
        if key == K_DOWN:
            if rect.bottom < self.screen_size[1] - self.step:
                rect.top += self.step

        self.rect = rect
        print self.rect.center

    def fire(self, spritelist, image, screen):
        print "VUUR!"
        if self.timer < pygame.time.get_ticks():
            spritelist.add(Fireball(image, self.rect, screen))
            self.timer = pygame.time.get_ticks() + 500
