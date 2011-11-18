import pygame
import sys
from pygame.locals import *

pygame.mixer.pre_init(44100, -16, 2, 2048)

class SoundController(object):
    def __init__(self):
        pass

    def init_music(self, filename):
        pygame.mixer.music.load(filename)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    def load_sound(self, filename):
        return pygame.mixer.Sound(filename)

    def init_sounds(self):
        init_music("resources/Music.mp3")

        self.boss_hit = load_sound("resources/Boss_Hit.wav")
        self.baby_hit = load_sound("resources/Baby_Hit.wav")
        self.demon_hit = load_sound("resources/Demon_Hit.wav")
        self.dragon_hit = load_sound("resources/Dragon_Hit.wav")
