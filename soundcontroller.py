import pygame

from pygame.locals import *

#sound IDs
hit_boss_snd = 'hit_boss'
hit_baby_snd = 'hit_baby'
hit_by_demon_snd = 'hit_by_demon'
hit_demon_snd = 'hit_demon'
caught_baby_snd = 'caught_baby'

class SoundController(object):
    def __init__(self):
        self.sounds = {}
        self.init_music("resources/Music.mp3")
        self.init_sounds()

    def play_music(self):
        pygame.mixer.music.play(-1)

    def init_music(self, filename):
        pygame.mixer.music.load(filename)
        pygame.mixer.music.set_volume(0.4)

    def load_sound(self, filename):
        return pygame.mixer.Sound(filename)

    def init_sounds(self):
        self.sounds[hit_boss_snd] = self.load_sound("resources/Boss_Hit.wav")
        self.sounds[hit_baby_snd] = self.load_sound("resources/Baby_Hit.wav")
        self.sounds[hit_demon_snd] = self.load_sound("resources/Demon_Hit.wav")
        self.sounds[hit_by_demon_snd] = self.load_sound("resources/Dragon_Hit.wav")
        self.sounds[caught_baby_snd] = self.load_sound("resources/Baby_Caught.wav")

    def play_sound(self, snd_id):
        self.sounds[snd_id].play()
