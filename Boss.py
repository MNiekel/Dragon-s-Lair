import pygame
import sys
import time
import random
from pygame.locals import *

class Boss(pygame.sprite.Sprite):
    def __init__(self, image, image_hit, hit_sound, screen):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.image_normal = image
        self.image_hit = image_hit
        self.mask = pygame.mask.from_surface(image)

        self.screen = screen
        self.screen_size = screen.get_size()

        self.rect = self.image.get_rect()
        self.rect.topright = (self.screen_size[0] - 4, 200)

        self.direction = 1
        self.step = 8
        self.energy = 100
        self.sound_hit = hit_sound
        pygame.time.set_timer(DEMON_EVENT, random.randint(2500, 4500))
        pygame.time.set_timer(BABY_EVENT, random.randint(1500, 7500))

    def release_demon(self, spritelist, image, screen):
        pygame.time.set_timer(DEMON_EVENT, random.randint(2500, 4500))
        print "DEMON!"
        spritelist.add(Demon(image, self.rect, screen))

    def release_baby(self, spritelist, image, screen):
        pygame.time.set_timer(BABY_EVENT, random.randint(1500, 7500))
        print "BABY!"
        spritelist.add(Baby(image, self.rect, screen))

    def change_colour(self):
        if (self.image == self.image_hit):
            self.image = self.image_normal
        else:
            self.image = self.image_hit

    def hit(self):
        self.sound_hit.play()
        self.energy -= 10
        self.change_colour()
        pygame.time.set_timer(BOSSFLASH_EVENT, 50)

    def update(self):
        if self.direction == 1:
            #move_up
            self.rect.top -= self.step
            if self.rect.top < 0:
                self.direction = -1
        elif self.direction == -1:
            #move_down
            self.rect.top += self.step
            if self.rect.bottom >= self.screen_size[1]:
                self.direction = 1
