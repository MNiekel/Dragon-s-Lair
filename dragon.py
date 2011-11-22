import pygame
import mysprite

from pygame.locals import *

STARTPOS = (4, 200)
MAXLIVES = 3
STEP = 8

FIREBALL_STEP = 12
FIREREPEAT = 500

HIT_BY_DEMON_PTS = -5
CAUGHT_BABY_PTS = 10
HIT_BABY_PTS = -20
HIT_DEMON_PTS = 10
KILLED_BOSS_PTS = 100

class Dragon(mysprite.MySprite):
    def __init__(self, image, screen):
        mysprite.MySprite.__init__(self, image, screen)

        self.rect.topleft = STARTPOS
        self.step = STEP
        self.lives = MAXLIVES
        self.timer = 0
        self.score = 0

    def reset(self):
        self.rect.topleft = STARTPOS
        self.lives = MAXLIVES
        self.timer = 0
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
            self.timer = pygame.time.get_ticks() + FIREREPEAT
            return Fireball(image, self.screen, self.rect)
        else:
            return None

    def hit_by_demon(self):
        self.lives -= 1
        if self.lives <= 0:
            print "GAME OVER"
            return True
        self.score = max(0, self.score + HIT_BY_DEMON_PTS)
        return False

    def hit_baby(self):
        self.score = max(0, self.score + HIT_BABY_PTS)

    def hit_demon(self):
        self.score += HIT_DEMON_PTS

    def caught_baby(self):
        self.score += CAUGHT_BABY_PTS

class Fireball(mysprite.MySprite):
    def __init__(self, image, screen, position):
        mysprite.MySprite.__init__(self, image, screen)

        self.rect.left = position.right
        self.rect.top = position.top
        self.step = FIREBALL_STEP

    def update(self):
        self.rect.left += self.step
        if self.rect.right > self.screen_size[0]:
            self.kill()
            del self
