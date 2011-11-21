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
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()
        pygame.key.set_repeat(1)
        self.screen = pygame.display.set_mode(size)
        self.timer = 0

    def initialize(self):
        self.sounds = soundcontroller.SoundController()
        self.images = imagecontroller.ImageController()

        self.background = self.images.get_background()

        self.stats = stats.Stats(self.screen, self.images.get_image(heart_img))
        self.dragon = dragon.Dragon(self.images.get_image(dragon_img), self.screen)
        self.boss = boss.Boss(self.images.get_image(boss_img), self.images.get_image(boss_hit_img), self.screen)

        self.rendering = pygame.sprite.RenderUpdates()
        self.fireballs = pygame.sprite.RenderUpdates()
        self.demons = pygame.sprite.RenderUpdates()
        self.babies = pygame.sprite.RenderUpdates()

        self.rendering.add(self.dragon)
        self.rendering.add(self.boss)

        self.sounds.play_music()

    def clear_screen(self):
        self.screen.blit(self.background, [0, 0])
        pygame.display.flip()

    def release_demon(self):
        self.boss.release_demon(self.demons, self.images.get_image(demon_img),
            self.screen)

    def release_baby(self):
        self.boss.release_baby(self.babies, self.images.get_image(baby_img),
            self.screen)

    def move_dragon(self, key):
        self.dragon.move(key)

    def fire_fireball(self):
        fireball = self.dragon.fire(self.images.get_image(fireball_img))
        if fireball != None:
            self.fireballs.add(fireball)

    def control_volume(self, key):
        if key == K_m:
            self.sounds.toggle_music()
        if key == K_d:
            self.sounds.volume_down()
        if key == K_u:
            self.sounds.volume_up()

    def update_gameobjects(self):
        self.rendering.update()
        self.fireballs.update()
        self.demons.update()
        self.babies.update()
        self.stats.update(self.dragon, self.boss)

    def update_display(self):
        pygame.display.update(self.rendering.draw(self.screen))
        pygame.display.update(self.fireballs.draw(self.screen))
        pygame.display.update(self.demons.draw(self.screen))
        pygame.display.update(self.babies.draw(self.screen))

        self.screen.blit(self.background, [0, 0])

    def collide(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, True, pygame.sprite.collide_mask)

    def groupcollide(self, group1, group2):
        return pygame.sprite.groupcollide(group1, group2, True, True)

    def check_collisions(self):
        killed = False
        killed_boss = False

        if self.collide(self.dragon, self.demons):
            print "#hit by demon"
            killed = self.dragon.hit_by_demon()
            self.sounds.play_sound(hit_by_demon_snd)
        if self.collide(self.dragon, self.babies):
            print "#caught baby"
            self.dragon.caught_baby()
            self.sounds.play_sound(caught_baby_snd)
        if self.collide(self.boss, self.fireballs):
            print "#hit boss"
            killed_boss = self.boss.hit()
            if killed_boss:
                time = (pygame.time.get_ticks() - self.timer) / 1000
                self.dragon.killed_boss(time)
            self.sounds.play_sound(hit_boss_snd)
        if self.groupcollide(self.fireballs, self.demons):
            print "#hit demon"
            self.dragon.hit_demon()
            self.sounds.play_sound(hit_demon_snd)
        if self.groupcollide(self.fireballs, self.babies):
            print "#hit baby"
            self.dragon.hit_baby()
            self.sounds.play_sound(hit_baby_snd)

        return (killed or killed_boss)

    def start_screen(self):
        self.clear_screen()
        title = self.images.load_image("resources/Title.gif")
        self.screen.blit(title, [0, 0])
        controls = self.images.load_image("resources/Controls.gif")
        self.screen.blit(controls, [0, 200])
        text = textsurface.TextSurface("Press <SPACE> to Start")
        rect = text.get_rect()
        width = rect.width
        height = rect.height
        xpos = (self.screen.get_width() - rect.width) / 2
        ypos = self.screen.get_height() - height * 2
        text.set_position((xpos, ypos), self.screen)
        self.screen.blit(text, text.get_rect())
        pygame.display.flip()
        pygame.event.clear()
        while True:
            event = pygame.event.poll()
            if (event.type == KEYUP and event.key == K_SPACE):
                pygame.event.clear()
                self.clear_screen()
                self.timer = pygame.time.get_ticks()
                return True
            if (event.type == KEYDOWN and event.key == K_ESCAPE):
                return False

    def end_screen(self):
        self.clear_screen()
        game_over = self.images.load_image("resources/Game_Over.gif")
        self.screen.blit(game_over, [0, 0])
        text = textsurface.TextSurface("Your Score: "+str(self.dragon.score))
        rect = text.get_rect()
        width = rect.width
        height = rect.height
        xpos = (self.screen.get_width() - rect.width) / 2
        ypos = self.screen.get_height() - height * 6
        text.set_position((xpos, ypos), self.screen)
        self.screen.blit(text, text.get_rect())
        pygame.display.flip()
        pygame.event.clear()
        while True:
            event = pygame.event.poll()
            if (event.type == KEYUP and event.key == K_SPACE):
                sys.exit()
                break
