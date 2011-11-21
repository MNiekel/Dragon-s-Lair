import pygame
import mysprite
import random

from pygame.locals import *
from globals import *

YPOS = 200
XPOS = 4
STEP = 8
DIRECTION = 1
MAXENERGY = 100 #procent

DEMON_MININTERVAL = 2500
DEMON_MAXINTERVAL = 4500
BABY_MININTERVAL = 1500
BABY_MAXINTERVAL = 7500
HEAL_INTERVAL = 50

DEMON_XSTEP = 4
DEMON_YSTEP = 2
BABY_STEP = 6

class Boss(mysprite.MySprite):
    def __init__(self, image, altimage, screen):
        mysprite.MySprite.__init__(self, image, screen)

        self.rect.topright = (self.screen_size[0] - XPOS, YPOS)
        self.altimage = altimage
        self.step = STEP
        self.direction = DIRECTION
        self.energy = MAXENERGY
        self.flash = -1
        self.autoheal = HEAL_INTERVAL #heal every autoheal updates

        pygame.time.set_timer(DEMON_EVENT,
            random.randint(DEMON_MININTERVAL, DEMON_MAXINTERVAL))
        pygame.time.set_timer(BABY_EVENT,
            random.randint(BABY_MININTERVAL, BABY_MAXINTERVAL))

    def reset(self):
        self.rect.topright = (self.screen_size[0] - XPOS, YPOS)
        self.direction = DIRECTION
        self.energy = MAXENERGY
        self.flash = -1

    def release_demon(self, spritelist, image, screen):
        pygame.time.set_timer(DEMON_EVENT,
            random.randint(DEMON_MININTERVAL, DEMON_MAXINTERVAL))
        spritelist.add(Demon(image, self.rect, screen))

    def release_baby(self, spritelist, image, screen):
        pygame.time.set_timer(BABY_EVENT,
            random.randint(BABY_MININTERVAL, BABY_MAXINTERVAL))
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
            return True
        self.change_colour()
        self.flash = 1
        return False

    def update(self):
        if self.flash == 0:
            self.change_colour()
            self.flash = -1
        elif self.flash > 0:
            self.flash -= 1

        if self.autoheal < 0:
            self.energy += 1
            self.autoheal = HEAL_INTERVAL
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
        self.step = BABY_STEP

    def update(self):
        self.rect.right -= self.step
        if self.rect.centerx < 0:
            self.kill()
            del self

class Demon(mysprite.MySprite):
    def __init__(self, image, position, screen):
        mysprite.MySprite.__init__(self, image, screen)
        self.yspeed = random.randint(-DEMON_YSTEP, DEMON_YSTEP)
        self.rect.right = position.left
        self.rect.top = max(position.top, 0)
        self.step = DEMON_XSTEP

    def update(self):
        self.rect.right -= self.step
        self.rect.top = self.rect.top + self.step * self.yspeed
        if (self.rect.bottom > self.screen_size[1] or self.rect.top < 0):
            self.yspeed = -self.yspeed
        if self.rect.centerx < 0:
            self.kill()
            del self
