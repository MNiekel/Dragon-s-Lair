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
import gamecontroller

from globals import *
from pygame.locals import *
from soundcontroller import *
from imagecontroller import *

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
pygame.key.set_repeat(1)
clock = pygame.time.Clock()

def restart_game(screen, dragon, boss, fireballs, demons, babies, stats):
    dragon.reset()
    boss.reset()
    screen.blit(background, [0, 0])
    pygame.display.flip()
    stats.update(dragon, boss)
    demons.empty()
    fireballs.empty()
    babies.empty()
    pygame.event.clear()

def end_screen(screen, dragon, boss):
    game_over = textsurface.TextSurface("GAME OVER!", RED, TRANSPARENT, 64)
    rect = game_over.get_rect()
    width = rect.width
    height = rect.height
    xpos = (screen.get_width() - rect.width) / 2
    ypos = screen.get_height() / 2 - height
    game_over.set_position((xpos, ypos), screen)
    screen.blit(background, [0, 0])
    screen.blit(game_over, game_over.get_rect())
    pygame.display.flip()
    pygame.event.clear()
    while True:
        event = pygame.event.poll()
        if (event.type == KEYUP and event.key == K_SPACE):
            break

#game = gamecontroller.Game(PANDORA)
#game.initialize()

screen = pygame.display.set_mode(PANDORA)

sounds = soundcontroller.SoundController()
images = imagecontroller.ImageController()

background = images.get_background()
screen.blit(background, [0, 0])

stats = stats.Stats(screen, images.get_image(heart_img))

dragon = dragon.Dragon(images.get_image(dragon_img), screen)
boss = boss.Boss(images.get_image(boss_img), images.get_image(boss_hit_img), screen)

rendering = pygame.sprite.RenderUpdates()
fireballs = pygame.sprite.RenderUpdates()
demons = pygame.sprite.RenderUpdates()
babies = pygame.sprite.RenderUpdates()

rendering.add(dragon)
rendering.add(boss)

pygame.display.flip()
sounds.play_music()
#pygame.time.wait(2000)
#sys.exit()

while True:
    clock.tick(30)

    for event in pygame.event.get():
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

    #game.update()
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

    #collision = game.collisions()
    #case collision.type ==
    if (pygame.sprite.spritecollide(dragon, demons, True, None)):
        print "#hit by demon"
        killed = dragon.hit_by_demon()
        sounds.play_sound(hit_by_demon_snd)
        if killed:
            stats.update(dragon, boss)
            pygame.time.wait(1000)
            end_screen(screen, dragon, boss)
            restart_game(screen, dragon, boss, fireballs, demons, babies, stats)
    if (pygame.sprite.spritecollide(dragon, babies, True, None)):
        print "#caught baby"
        dragon.caught_baby()
        sounds.play_sound(caught_baby_snd)
    if (pygame.sprite.spritecollide(boss, fireballs, True, pygame.sprite.collide_mask)):
        print "#hit boss"
        boss.hit()
        sounds.play_sound(hit_boss_snd)
    if (pygame.sprite.groupcollide(fireballs, demons, True, True)):
        print "#hit demon"
        dragon.hit_demon()
        sounds.play_sound(hit_demon_snd)
    if (pygame.sprite.groupcollide(fireballs, babies, True, True)):
        print "#hit baby"
        dragon.hit_baby()
        sounds.play_sound(hit_baby_snd)
