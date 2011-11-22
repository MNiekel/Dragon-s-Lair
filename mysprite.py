import pygame

from pygame.locals import *

class MySprite(pygame.sprite.Sprite):
    def __init__(self, image, screen):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.mask = pygame.mask.from_surface(image)
        self.rect = self.image.get_rect()
        self.screen = screen
        self.screen_size = screen.get_size()

    def get_rect(self):
        return self.image.get_rect()
