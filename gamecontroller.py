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

    def initialize(self):
        self.sounds = soundcontroller.SoundController()
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

    def clear_screen(self):
        self.screen.blit(self.background, [0, 0])
        pygame.display.flip()

    def update_gameobjects(self):
        self.rendering.update()
        self.fireballs.update()
        self.demons.update()
        self.babies.update()
        self.stats.update(dragon, boss)

    def restart(self):
        self.dragon.reset()
        self.boss.reset()
        self.screen.blit(self.background, [0, 0])
        pygame.display.flip()
        self.stats.update(dragon, boss)
        self.demons.empty()
        self.fireballs.empty()
        self.babies.empty()
        pygame.event.clear()

    def evaluate_event(self, event):
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == DEMON_EVENT:
            boss.release_demon(demons, images.get_image(demon_img), screen)
            #game.release_demon()

        elif event.type == BABY_EVENT:
            boss.release_baby(babies, images.get_image(baby_img), screen)
            #game.release_baby()

        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()
            if event.key in (K_UP, K_DOWN):
                dragon.move(event.key)
            if event.key == K_SPACE:
                #game.fireball()
                fireball = dragon.fire(images.get_image(fireball_img))
                if fireball != None:
                    fireballs.add(fireball)

        elif event.type == KEYUP:
            if event.key == K_m:
                sounds.toggle_music()
            if event.key == K_u:
                sounds.volume_up()
            if event.key == K_d:
                sounds.volume_down()

    def check_collisions(self):
        killed = False
        killed_boss = False

        if (pygame.sprite.spritecollide(self.dragon, self.demons, True, None)):
            print "#hit by demon"
            killed = self.dragon.hit_by_demon()
            self.sounds.play_sound(hit_by_demon_snd)
        if (pygame.sprite.spritecollide(self.dragon, self.babies, True, None)):
            print "#caught baby"
            self.dragon.caught_baby()
            self.sounds.play_sound(caught_baby_snd)
        if (pygame.sprite.spritecollide(self.boss, self.fireballs, True, pygame.sprite.collide_mask)):
            print "#hit boss"
            killed_boss = self.boss.hit()
            self.sounds.play_sound(hit_boss_snd)
        if (pygame.sprite.groupcollide(self.fireballs, self.demons, True, True)):
            print "#hit demon"
            self.dragon.hit_demon()
            self.sounds.play_sound(hit_demon_snd)
        if (pygame.sprite.groupcollide(self.fireballs, self.babies, True, True)):
            print "#hit baby"
            self.dragon.hit_baby()
            self.sounds.play_sound(hit_baby_snd)

        return (killed or killed_boss)

    def start_screen(self):
        self.clear_screen()
        title = self.images.load_image("resources/Title.gif")
        self.screen.blit(title, [0, 0])
        text = textsurface.TextSurface("Press <SPACE> to Start")
        rect = text.get_rect()
        width = rect.width
        height = rect.height
        xpos = (self.screen.get_width() - rect.width) / 2
        ypos = self.screen.get_height() - height
        text.set_position((xpos, ypos), self.screen)
        self.screen.blit(text, text.get_rect())
        pygame.display.flip()
        pygame.event.clear()
        while True:
            event = pygame.event.poll()
            if (event.type == KEYUP and event.key == K_SPACE):
                pygame.event.clear()
                self.clear_screen()
                break

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
