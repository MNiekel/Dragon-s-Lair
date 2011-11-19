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

screen, background = init_screen(PANDORA)

sound = soundcontroller.SoundController()
images = imagecontroller.ImageController()
dragon_img, boss_img, boss_hit_img, fireball_img, demon_img, baby_img, heart_img = images.get_images()

stats = stats.Stats(screen, heart_img)
pygame.display.flip()

sound.play_music()
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
            if event.key == K_a:
                #pygame.display.update(tekstje.get_rect())
                #print tekstje.get_rect()
                dragon.lives = 5

        elif event.type == KEYUP:
            if event.key == K_m:
                sound.toggle_music()
            if event.key == K_u:
                sound.volume_up()
            if event.key == K_d:
                sound.volume_down()

    rendering.update()
    fireballs.update()
    demons.update()
    babies.update()
    stats.update(dragon, boss)

    pygame.display.update(rendering.draw(screen))
    pygame.display.update(fireballs.draw(screen))
    pygame.display.update(demons.draw(screen))
    pygame.display.update(babies.draw(screen))

    screen.blit(background, [0, 0])

    if (pygame.sprite.spritecollide(dragon, demons, True, None)):
        print "#hit by demon"
        killed = dragon.hit_by_demon()
        sound.play_sound(hit_by_demon_snd)
        if killed:
            stats.update(dragon, boss)
            pygame.time.wait(5000)
            sys.exit()
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
