import pygame
import textsurface

from pygame.locals import *
from globals import *

class Stats(object):
    def __init__(self, screen):
        self.lives = Lives(screen)
        self.score = Score(screen)
        self.healthbar = Healthbar(screen)
        self.screen = screen

    def update(self, dragon, boss):
        self.score.update(dragon.score)
        self.healthbar.update(boss.rect, boss.energy)
        self.lives.update(dragon.lives)

class Healthbar(pygame.Surface):
    def __init__(self, screen):
        self.width = 120
        self.height = 8
        self.size = (self.width, self.height)
        pygame.Surface.__init__(self, self.size)
        self.convert()
        self.set_colorkey(TRANSPARENT)

        self.screen = screen

    def update(self, bossrect, health):
        health = min(100, health)

        x = (255 * health)/50 - 255

        if (health > 50):
            col = 255 - x, 255, 0
        elif (health > 8):
            col = 255, 255 + x, 0
        else:
            col = RED

        self.fill(TRANSPARENT)
        self.fill(col, Rect(0, 0, health * self.width / 100, 8))

        rect = self.get_rect()
        pygame.display.update(rect)

        rect.left = bossrect.left
        rect.bottom = bossrect.bottom

        self.screen.blit(self, rect)

class Score(pygame.Surface):
    def __init__(self, screen):
        self.font = pygame.font.SysFont('Comic Sans MS', 24)
        pygame.Surface.__init__(self, self.font.size("Score: 0000"))

        surface = textsurface.TextSurface("Score: ", WHITE)
        self.screen = screen

        self.rect = self.get_rect()
        self.text_rect = surface.get_rect()
        self.text_rect.topleft = (0, 0)

        left = self.text_rect.right
        width = self.rect.right - self.text_rect.right
        self.score_rect = Rect(left, self.rect.top, width, self.rect.height)

        self.fill(TRANSPARENT)
        self.set_colorkey(TRANSPARENT)

        self.blit(surface, self.text_rect)
        self.screen.blit(self, self.text_rect)

    def update(self, score):
        surface = textsurface.TextSurface(str(score))
        rect = surface.get_rect()
        rect.bottomright = self.get_rect().bottomright

        self.fill(TRANSPARENT, self.score_rect)

        self.blit(surface, rect)
        self.screen.blit(self, self.rect)
        pygame.display.update(self.score_rect)


class Lives(object):
    def __init__(self, screen):
        self.font = pygame.font.SysFont('Comic Sans MS', 24)
        self.text = textsurface.TextSurface("Lives: ", WHITE)
        self.screen = screen
        self.text.set_position((200, 0), self.screen)

        self.screen.blit(self.text, self.text.get_rect())

        self.heart = pygame.Surface((32, 32)).convert()
        self.heart.set_colorkey(TRANSPARENT)
        self.heart.fill(RED)
        self.heartrect = self.heart.get_rect()
        #self.heartrect.topleft = self.text.get_rect().topright

    def update(self, lives):
        self.screen.blit(self.text, self.text.get_rect())
        pygame.display.update(self.text.get_rect())
        self.heart.fill(RED)
        rect = self.heartrect
        rect.topleft = self.text.get_rect().topright
        for i in range(0, 3):
            if (i < lives):
                self.screen.blit(self.heart, self.heartrect)
                pygame.display.update(rect)
                rect.topleft = rect.topright
            else:
                self.heart.fill(TRANSPARENT)
                self.screen.blit(self.heart, self.heartrect)
                pygame.display.update(rect)
                rect.topleft = rect.topright
