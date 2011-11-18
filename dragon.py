import pygame
import mysprite
import random

from pygame.locals import *
from globals import *

class Dragon(mysprite.MySprite):
    def __init__(self, image, screen):
        mysprite.MySprite.__init__(self, image, screen)

        self.rect.topleft = (4, 200)
        self.step = 8
        self.timer = 0
        self.lives = 3
        self.score = 0

    def move(self, key):
        rect = self.rect

        if key == K_UP:
            if rect.top > self.step:
                rect.top -= self.step
        if key == K_DOWN:
            if rect.bottom < self.screen_size[1] - self.step:
                rect.top += self.step

        self.rect = rect

    def fire(self, image):
        if self.timer < pygame.time.get_ticks():
            self.timer = pygame.time.get_ticks() + 500
            return Fireball(image, self.screen, self.rect)
        else:
            return None

    def hit(self):
        self.lives -= 1
        if self.lives < 0:
            print "GAME OVER"
            pygame.event.post(pygame.event.Event(QUIT))

    def set_score(self, points):
        self.score += points
        self.score = max(0, self.score)

    def hit_by_demon(self):
        self.lives -= 1
        if self.lives < 0:
            print "GAME OVER"
            pygame.event.post(pygame.event.Event(QUIT))
        self.score = max(0, self.score - 10)

    def hit_baby(self):
        self.score = max(0, self.score - 20)

    def hit_demon(self):
        self.score += 5

    def caught_baby(self):
        self.score += 10

class Fireball(mysprite.MySprite):
    def __init__(self, image, screen, position):
        mysprite.MySprite.__init__(self, image, screen)

        self.rect.left = position.right
        self.rect.top = position.top
        self.step = 12

    def update(self):
        self.rect.left += self.step
        if self.rect.right > self.screen_size[0]:
            self.kill()
            del self
