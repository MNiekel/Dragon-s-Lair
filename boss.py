import pygame
import mysprite
import random

from pygame.locals import *
from globals import *

class Boss(mysprite.MySprite):
    def __init__(self, image, altimage, screen):
        mysprite.MySprite.__init__(self, image, screen)

        self.rect.topright = (self.screen_size[0] - 4, 200)
        self.altimage = altimage
        self.direction = 1
        self.step = 8
        self.energy = 100
        self.flash = -1
        self.autoheal = 50 #heal every autoheal updates

        pygame.time.set_timer(DEMON_EVENT, random.randint(2500, 4500))
        pygame.time.set_timer(BABY_EVENT, random.randint(1500, 7500))

    def release_demon(self, spritelist, image, screen):
        pygame.time.set_timer(DEMON_EVENT, random.randint(2500, 4500))
        spritelist.add(Demon(image, self.rect, screen))

    def release_baby(self, spritelist, image, screen):
        pygame.time.set_timer(BABY_EVENT, random.randint(1500, 7500))
        spritelist.add(Baby(image, self.rect, screen))

    def change_colour(self):
        img = self.image
        self.image = self.altimage
        self.altimage = img

    def set_energy(self, d):
        self.energy = min(100, self.energy + d)

    def hit(self):
        self.energy = min(100, self.energy - 10)
        if self.energy <= 0:
            print "You defeated the Boss"
            pygame.event.post(pygame.event.Event(QUIT))
        self.change_colour()
        self.flash = 1

    def update(self):
        if self.flash == 0:
            self.change_colour()
            self.flash = -1
        elif self.flash > 0:
            self.flash -= 1

        if self.autoheal < 0:
            self.energy += 1
            self.autoheal = 50
        else:
            self.autoheal -= 1

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

class Baby(mysprite.MySprite):
    def __init__(self, image, position, screen):
        mysprite.MySprite.__init__(self, image, screen)
        self.rect.right = position.left
        self.rect.top = max(position.top, 0)
        self.step = 6

    def update(self):
        self.rect.right -= self.step
        if self.rect.centerx < 0:
            self.kill()
            del self

class Demon(mysprite.MySprite):
    def __init__(self, image, position, screen):
        mysprite.MySprite.__init__(self, image, screen)
        self.yspeed = random.randint(-2, 2)
        self.rect.right = position.left
        self.rect.top = max(position.top, 0)
        self.step = 4

    def update(self):
        self.rect.right -= self.step
        self.rect.top = self.rect.top + self.step * self.yspeed
        if (self.rect.bottom > self.screen_size[1] or self.rect.top < 0):
            self.yspeed = -self.yspeed
        if self.rect.centerx < 0:
            self.kill()
            del self
