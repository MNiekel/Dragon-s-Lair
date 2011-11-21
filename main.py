import pygame
import sys
import time
import random
import soundcontroller
import imagecontroller
import gamecontroller

from globals import *
from pygame.locals import *
from soundcontroller import *
from imagecontroller import *

game = gamecontroller.Game(PANDORA)
game.initialize()

clock = pygame.time.Clock()
sounds = soundcontroller.SoundController()
images = imagecontroller.ImageController()

sounds.play_music()
game.start_screen()

gameover = False

while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        #game.evaluate_event(event)
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

    #game.update_gameobjects()
    rendering.update()
    fireballs.update()
    demons.update()
    babies.update()
    stats.update(dragon, boss)

    #game.update_display()
    pygame.display.update(rendering.draw(screen))
    pygame.display.update(fireballs.draw(screen))
    pygame.display.update(demons.draw(screen))
    pygame.display.update(babies.draw(screen))

    screen.blit(background, [0, 0])

    gameover = collisions(dragon, boss, demons, babies, fireballs)
    if gameover:
        stats.update(dragon, boss)
        pygame.time.wait(1000)
        end_screen(screen, dragon, boss)
        restart_game(screen, dragon, boss, fireballs, demons, babies, stats)
