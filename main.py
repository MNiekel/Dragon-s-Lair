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

if not game.start_screen():
    sys.exit()

while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == DEMON_EVENT:
            game.release_demon()

        elif event.type == BABY_EVENT:
            game.release_baby()

        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()
            if event.key in (K_UP, K_DOWN):
                game.move_dragon(event.key)
            if event.key == K_SPACE:
                game.fire_fireball()

        elif event.type == KEYUP:
            if ((event.key == K_u) or (event.key == K_d) or (event.key == K_m)):
                game.control_volume(event.key)

    game.update_gameobjects()
    game.update_display()

    gameover = game.check_collisions()

    if gameover:
        pygame.time.wait(1000)
        game.end_screen()
