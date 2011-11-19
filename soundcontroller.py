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
        self.music = False
        self.pause = False

    def play_music(self):
        pygame.mixer.music.play(-1)
        self.music = True

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

    def toggle_music(self):
        if self.music:
            if self.pause:
                pygame.mixer.music.unpause()
                self.pause = False
            else:
                pygame.mixer.music.pause()
                self.pause = True

    def volume_up(self):
        volume = self.sounds[hit_boss_snd].get_volume()
        if (volume < 1.0):
            volume = min(volume+0.1, 1.0)
            self.sounds[hit_boss_snd].set_volume(volume)
            self.sounds[hit_baby_snd].set_volume(volume)
            self.sounds[hit_demon_snd].set_volume(volume)
            self.sounds[hit_by_demon_snd].set_volume(volume)
            self.sounds[caught_baby_snd].set_volume(volume)
        print volume

    def volume_down(self):
        volume = self.sounds[hit_boss_snd].get_volume()
        if (volume > 0.0):
            volume = max(volume-0.1, 0.0)
            self.sounds[hit_boss_snd].set_volume(volume)
            self.sounds[hit_baby_snd].set_volume(volume)
            self.sounds[hit_demon_snd].set_volume(volume)
            self.sounds[hit_by_demon_snd].set_volume(volume)
            self.sounds[caught_baby_snd].set_volume(volume)
        print volume
