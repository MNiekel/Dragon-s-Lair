import pygame

from globals import *
from pygame.locals import *

class TextSurface(pygame.Surface):
    def __init__(self, text, color = WHITE, bgcolor = TRANSPARENT,
                fontsize = 24, fonttype = 'Comic Sans MS'):

        self.font = pygame.font.SysFont(fonttype, fontsize)
        self.size = self.font.size(text)
        self.text = text
        self.color = color
        self.bgcolor = bgcolor

        pygame.Surface.__init__(self, self.size)

        self.rect = pygame.Surface.get_rect(self)
        self.text = self.font.render(text, False, color, bgcolor).convert()
        rect = self.text.get_rect()
        rect.topleft = (0, 0)
        self.set_colorkey(TRANSPARENT)
        self.blit(self.text, rect)

    def set_position(self, pos, screen):
        self.rect.topleft = pos

    def get_rect(self):
        return self.rect

    def update(self, screen):
        screen.blit(self, self.rect)
