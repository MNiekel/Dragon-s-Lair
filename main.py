import pygame
import sys
import time
import random
import mysprite
import boss
import dragon
from globals import *
from pygame.locals import *

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

def load_image(file):
    img = pygame.image.load(file).convert()
    img.set_colorkey(TRANSPARENT)

    return img

def init_images():
    dragon = load_image("resources/Dragon.gif")
    boss = load_image("resources/Boss.gif")
    boss_hit = load_image("resources/Boss_Hit.gif")
    fireball = load_image("resources/Fireball.gif")
    demon = load_image("resources/Demon2.gif")
    baby = load_image("resources/Baby.gif")

    return dragon, boss, boss_hit, fireball, demon, baby

def init_music(filename):
    pygame.mixer.music.load(filename)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

def load_sound(filename):
    return pygame.mixer.Sound(filename)

def init_sounds():
    init_music("resources/Music.mp3")

    boss_hit = load_sound("resources/Boss_Hit.wav")
    baby_hit = load_sound("resources/Baby_Hit.wav")
    demon_hit = load_sound("resources/Demon_Hit.wav")
    dragon_hit = load_sound("resources/Dragon_Hit.wav")

    return boss_hit, baby_hit, demon_hit, dragon_hit

class Healthbar(pygame.Surface):
    def __init__(self, screen):
        pygame.Surface.__init__(self, (100, 8))
        self.convert()
        self.set_colorkey(TRANSPARENT)

        self.screen = screen

    def update(self, bossrect, health):
        health = min(100, health)

        x = (255 * health)/50 - 255

        if (health > 50):
            col = 255 - x, 255, 0
        elif (health > 10):
            col = 255, 255 + x, 0
        else:
            col = RED

        self.fill(TRANSPARENT)
        self.fill(col, Rect(0, 0, health, 8))

        rect = self.get_rect()
        pygame.display.update(rect)

        rect.left = bossrect.left
        rect.bottom = bossrect.bottom

        self.screen.blit(self, rect)

class Text(pygame.Surface):
    def __init__(self, text, color = WHITE,
                fonttype = 'Comic Sans MS', fontsize = 24):

        self.font = pygame.font.SysFont(fonttype, fontsize)
        self.size = self.font.size(text)
        self.text = text
        self.color = color

        pygame.Surface.__init__(self, self.size)

        surface = self.font.render(text, False, color, TRANSPARENT)
        rect = surface.get_rect()
        rect.topleft = (0, 0)
        self.set_colorkey(TRANSPARENT)
        self.blit(surface, rect)

class Score(pygame.Surface):
    def __init__(self, screen):
        self.font = pygame.font.SysFont('Comic Sans MS', 24)
        pygame.Surface.__init__(self, self.font.size("Score: 0000"))

        surface = Text("Score: ", WHITE)

        self.rect = self.get_rect()
        self.text_rect = surface.get_rect()
        self.text_rect.topleft = (0, 0)

        left = self.text_rect.right
        width = self.rect.right - self.text_rect.right
        self.score_rect = Rect(left, self.rect.top, width, self.rect.height)

        self.fill(TRANSPARENT)
        self.set_colorkey(TRANSPARENT)

        self.blit(surface, self.text_rect)
        screen.blit(self, self.text_rect)

    def update(self, score):
        surface = Text(str(score))
        #surface = self.font.render(str(score), False, WHITE, TRANSPARENT)
        rect = surface.get_rect()
        rect.bottomright = self.get_rect().bottomright

        self.fill(TRANSPARENT, self.score_rect)

        self.blit(surface, rect)
        screen.blit(self, self.rect)
        pygame.display.update(self.score_rect)

screen, background = init_screen(PANDORA)
score = Score(screen)

pygame.display.flip()
dragon_img, boss_img, boss_hit_img, fireball_img, demon_img, baby_img = init_images()
boss_hit_snd, baby_hit_snd, demon_hit_snd, dragon_hit_snd = init_sounds()
rendering = pygame.sprite.RenderUpdates()

dragon = dragon.Dragon(dragon_img, screen)
boss = boss.Boss(boss_img, boss_hit_img, screen)

healthbar = Healthbar(screen)

rendering.add(dragon)
rendering.add(boss)

fireballs = pygame.sprite.RenderUpdates()
demons = pygame.sprite.RenderUpdates()
babies = pygame.sprite.RenderUpdates()

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
        dragon_hit_snd.play()
    if (pygame.sprite.spritecollide(dragon, babies, True, None)):
        print "#caught baby"
        dragon.caught_baby()
    if (pygame.sprite.spritecollide(boss, fireballs, True, pygame.sprite.collide_mask)):
        print "#hit boss"
        boss.hit()
        boss_hit_snd.play()
    if (pygame.sprite.groupcollide(fireballs, demons, True, True)):
        print "#hit demon"
        dragon.hit_demon()
        demon_hit_snd.play()
    if (pygame.sprite.groupcollide(fireballs, babies, True, True)):
        print "#hit baby"
        dragon.hit_baby()
        baby_hit_snd.play()
