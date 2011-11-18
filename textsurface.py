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

        surface = self.font.render(text, False, color, bgcolor).convert()
        rect = surface.get_rect()
        rect.topleft = (0, 0)
        self.set_colorkey(TRANSPARENT)
        self.blit(surface, rect)
