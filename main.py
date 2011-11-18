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

from globals import *
from pygame.locals import *
from soundcontroller import *

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
pygame.key.set_repeat(1)
clock = pygame.time.Clock()

def init_screen(size):
    screen = pygame.display.set_mode(size)
    bg_image = pygame.image.load("resources/Background800x480.bmp").convert()
    background = pygame.Surface(size)
    screen.blit(bg_image, [0, 0])

    return screen, bg_image

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


screen, background = init_screen(PANDORA)
score = Score(screen)
healthbar = Healthbar(screen)
lives = textsurface.TextSurface("Lives: ")
screen.blit(lives, [300, 0])

pygame.display.flip()

sound = soundcontroller.SoundController()
images = imagecontroller.ImageController()

sound.play_music()
dragon_img, boss_img, boss_hit_img, fireball_img, demon_img, baby_img = images.get_images()

dragon = dragon.Dragon(dragon_img, screen)
boss = boss.Boss(boss_img, boss_hit_img, screen)

rendering = pygame.sprite.RenderUpdates()
fireballs = pygame.sprite.RenderUpdates()
demons = pygame.sprite.RenderUpdates()
babies = pygame.sprite.RenderUpdates()

rendering.add(dragon)
rendering.add(boss)

while True:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print dragon.score
            pygame.time.wait(5000)
            sys.exit()

        elif event.type == DEMON_EVENT:
            boss.release_demon(demons, demon_img, screen)

        elif event.type == BABY_EVENT:
            boss.release_baby(babies, baby_img, screen)

        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()
            if event.key in (K_UP, K_DOWN):
                dragon.move(event.key)
            if event.key == K_SPACE:
                fireball = dragon.fire(fireball_img)
                if fireball != None:
                    fireballs.add(fireball)

    rendering.update()
    fireballs.update()
    demons.update()
    babies.update()
    score.update(dragon.score)
    healthbar.update(boss.rect, boss.energy)

    pygame.display.update(rendering.draw(screen))
    pygame.display.update(fireballs.draw(screen))
    pygame.display.update(demons.draw(screen))
    pygame.display.update(babies.draw(screen))

    screen.blit(healthbar, [boss.rect.left, boss.rect.bottom])
    screen.blit(background, [0, 0])
    screen.blit(score, [0, 0])

    if (pygame.sprite.spritecollide(dragon, demons, True, None)):
        print "#hit by demon"
        dragon.hit_by_demon()
        sound.play_sound(hit_by_demon_snd)
    if (pygame.sprite.spritecollide(dragon, babies, True, None)):
        print "#caught baby"
        dragon.caught_baby()
        sound.play_sound(caught_baby_snd)
    if (pygame.sprite.spritecollide(boss, fireballs, True, pygame.sprite.collide_mask)):
        print "#hit boss"
        boss.hit()
        sound.play_sound(hit_boss_snd)
    if (pygame.sprite.groupcollide(fireballs, demons, True, True)):
        print "#hit demon"
        dragon.hit_demon()
        sound.play_sound(hit_demon_snd)
    if (pygame.sprite.groupcollide(fireballs, babies, True, True)):
        print "#hit baby"
        dragon.hit_baby()
        sound.play_sound(hit_baby_snd)
