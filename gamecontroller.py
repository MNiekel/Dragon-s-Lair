import pygame
import sys
import time
import random
import mysprite
import boss
import dragon
import soundcontroller
import imagecontroller
import textsurface
import stats

from globals import *
from pygame.locals import *
from soundcontroller import *
from imagecontroller import *

class Game(object):
    def __init__(self, size):
        self.screen = pygame.display.set_mode(size)

    def initialize(self):
        self.sound = soundcontroller.SoundController()
        self.images = imagecontroller.ImageController()

        self.background = self.images.get_background()
        self.screen.blit(self.background, [0, 0])

        self.stats = stats.Stats(self.screen, self.images.get_image(heart_img))

        self.dragon = dragon.Dragon(self.images.get_image(dragon_img), self.screen)
        self.boss = boss.Boss(self.images.get_image(boss_img), self.images.get_image(boss_hit_img), self.screen)

        self.rendering = pygame.sprite.RenderUpdates()
        self.fireballs = pygame.sprite.RenderUpdates()
        self.demons = pygame.sprite.RenderUpdates()
        self.babies = pygame.sprite.RenderUpdates()

        self.rendering.add(self.dragon)
        self.rendering.add(self.boss)

    def restart(self):
        self.dragon.reset()
        self.boss.reset()
        self.screen.blit(self.background, [0, 0])
        pygame.display.flip()
        stats.update(dragon, boss)
        demons.empty()
        fireballs.empty()
        babies.empty()
        pygame.event.clear()

    def start_screen(self):
        pass

    def end_screen(self):
        game_over = textsurface.TextSurface("GAME OVER!", RED, TRANSPARENT, 64)
        rect = game_over.get_rect()
        width = rect.width
        height = rect.height
        xpos = (self.screen.get_width() - rect.width) / 2
        ypos = self.screen.get_height() / 2 - height
        game_over.set_position((xpos, ypos), self.screen)
        self.screen.blit(self.background, [0, 0])
        self.screen.blit(game_over, game_over.get_rect())
        pygame.display.flip()
        pygame.event.clear()
        while True:
            event = pygame.event.poll()
            if (event.type == KEYUP and event.key == K_SPACE):
                break
