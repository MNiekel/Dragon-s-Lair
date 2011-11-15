import pygame
import sys
import time
import random
from pygame.locals import *

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
pygame.key.set_repeat(1)
clock = pygame.time.Clock()

BG_SIZE = 640, 480
PANDORA = 800, 480
DEMON_EVENT = USEREVENT+1
BABY_EVENT = USEREVENT+2
BOSSFLASH_EVENT = USEREVENT+3
TRANSPARENT = 0, 0, 255

images = {'DRAGON' : 0, 'BOSS' : 0, 'FIREBALL' : 0, 'DEMON' : 0, 'BABY' : 0}

def init_screen(size):
    black = 0, 0, 0
    screen = pygame.display.set_mode(size)
    bg_image = pygame.image.load("resources\Background800x480.bmp").convert()
    background = pygame.Surface(size)
    background.fill(black)
    background.blit(bg_image, [0, 0])
    screen.blit(background, [0, 0])

    return screen, background

def init_images():
    dragon = pygame.image.load("resources\Dragon.gif").convert()
    boss = pygame.image.load("resources\Boss.gif").convert()
    boss_hit = pygame.image.load("resources\Boss_Hit.gif").convert()
    fireball = pygame.image.load("resources\Fireball.gif").convert()
    demon = pygame.image.load("resources\Demon2.gif").convert()
    baby = pygame.image.load("resources\Baby.gif").convert()

    dragon.set_colorkey(TRANSPARENT)
    boss.set_colorkey(TRANSPARENT)
    boss_hit.set_colorkey(TRANSPARENT)
    fireball.set_colorkey(TRANSPARENT)
    demon.set_colorkey(TRANSPARENT)
    baby.set_colorkey(TRANSPARENT)

    return dragon, boss, boss_hit, fireball, demon, baby

def init_sound():
    music = pygame.mixer.music.load("resources\Music.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    try:
        boss_hit = pygame.mixer.Sound("resources\Boss_Hit.wav")
    except pygame.error, message:
        print 'Cannot load sound:', wav
        raise SystemExit, message
    return boss_hit

class Fireball(pygame.sprite.Sprite):
    def __init__(self, image, position, screen):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.mask = pygame.mask.from_surface(image)
        self.screen = screen
        self.screen_size = screen.get_size()
        self.rect = self.image.get_rect()
        self.rect.left = position.right
        self.rect.top = position.top
        self.step = 12

    def update(self):
        self.rect.left += self.step
        if self.rect.left > self.screen_size[0]:
            self.kill()
            del self

class Baby(pygame.sprite.Sprite):
    def __init__(self, image, position, screen):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.screen = screen
        self.screen_size = screen.get_size()
        self.rect = self.image.get_rect()
        self.rect.right = position.left
        self.rect.top = max(position.top, 0)
        self.step = 6

    def update(self):
        self.rect.right -= self.step
        if self.rect.right < 0:
            self.kill()
            del self

class Demon(pygame.sprite.Sprite):
    def __init__(self, image, position, screen):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.screen = screen
        self.screen_size = screen.get_size()
        self.rect = self.image.get_rect()
        self.yspeed = random.randint(-2, 2)
        self.rect.right = position.left
        self.rect.top = max(position.top, 0)
        self.step = 4

    def update(self):
        self.rect.right -= self.step
        self.rect.top = self.rect.top + self.step * self.yspeed
        if (self.rect.bottom > self.screen_size[1] or self.rect.top < 0):
            self.yspeed = -self.yspeed
        if self.rect.right < 0:
            self.kill()
            del self

class Boss(pygame.sprite.Sprite):
    def __init__(self, image, image_hit, hit_sound, screen):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.image_normal = image
        self.image_hit = image_hit
        self.mask = pygame.mask.from_surface(image)

        self.screen = screen
        self.screen_size = screen.get_size()

        self.rect = self.image.get_rect()
        self.rect.topright = (self.screen_size[0] - 4, 200)

        self.direction = 1
        self.step = 8
        self.energy = 100
        self.sound_hit = hit_sound
        pygame.time.set_timer(DEMON_EVENT, random.randint(2500, 4500))
        pygame.time.set_timer(BABY_EVENT, random.randint(1500, 7500))

    def release_demon(self, spritelist, image, screen):
        pygame.time.set_timer(DEMON_EVENT, random.randint(2500, 4500))
        print "DEMON!"
        spritelist.add(Demon(image, self.rect, screen))

    def release_baby(self, spritelist, image, screen):
        pygame.time.set_timer(BABY_EVENT, random.randint(1500, 7500))
        print "BABY!"
        spritelist.add(Baby(image, self.rect, screen))

    def change_colour(self):
        if (self.image == self.image_hit):
            self.image = self.image_normal
        else:
            self.image = self.image_hit

    def hit(self):
        self.sound_hit.play()
        self.energy -= 10
        self.change_colour()
        pygame.time.set_timer(BOSSFLASH_EVENT, 50)

    def update(self):
        if self.direction == 1:
            #move_up
            self.rect.top -= self.step
            if self.rect.top < 0:
                self.direction = -1
        elif self.direction == -1:
            #move_down
            self.rect.top += self.step
            if self.rect.bottom >= self.screen_size[1]:
                self.direction = 1

class Dragon(pygame.sprite.Sprite):
    def __init__(self, image, screen):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.screen = screen
        self.screen_size = screen.get_size()
        self.rect = self.image.get_rect()
        self.rect.topleft = (4, 200)
        self.step = 8
        self.timer = 0
        self.lives = 3

    def move(self, key):
        rect = self.rect

        if key == K_UP:
            if rect.top > self.step:
                rect.top -= self.step
        if key == K_DOWN:
            if rect.bottom < self.screen_size[1] - self.step:
                rect.top += self.step

        self.rect = rect

    def fire(self, spritelist, image, screen):
        print "VUUR!"
        if self.timer < pygame.time.get_ticks():
            spritelist.add(Fireball(image, self.rect, screen))
            self.timer = pygame.time.get_ticks() + 500

    def hit(self):
        print "AU!"
        self.lives -= 1
        if self.lives < 0:
            print "GAME OVER"
            pygame.event.post(pygame.event.Event(QUIT))

screen, background = init_screen(PANDORA)
pygame.display.flip()
dragon_img, boss_img, boss_hit_img, fireball_img, demon_img, baby_img = init_images()
boss_hit_snd = init_sound()
rendering = pygame.sprite.RenderUpdates()

dragon = Dragon(dragon_img, screen)
boss = Boss(boss_img, boss_hit_img, boss_hit_snd, screen)
rendering.add(dragon)
rendering.add(boss)
fireballs = pygame.sprite.RenderUpdates()
demons = pygame.sprite.RenderUpdates()
babies = pygame.sprite.RenderUpdates()

while True:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == DEMON_EVENT:
            boss.release_demon(demons, demon_img, screen)

        elif event.type == BABY_EVENT:
            boss.release_baby(babies, baby_img, screen)

        elif event.type == BOSSFLASH_EVENT:
            boss.change_colour()
            pygame.time.set_timer(BOSSFLASH_EVENT, 0)

        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()
            if event.key in (K_UP, K_DOWN):
                dragon.move(event.key)
            if event.key == K_SPACE:
                dragon.fire(fireballs, fireball_img, screen)

    rendering.update()
    fireballs.update()
    demons.update()
    babies.update()

    pygame.display.update(rendering.draw(screen))
    pygame.display.update(fireballs.draw(screen))
    pygame.display.update(demons.draw(screen))
    pygame.display.update(babies.draw(screen))
    screen.blit(background, [0, 0])

    if (pygame.sprite.spritecollide(dragon, demons, True, None)):
        print "#hit by demon"
        dragon.hit()
    if (pygame.sprite.spritecollide(dragon, babies, True, None)):
        print "#caught baby"
    if (pygame.sprite.spritecollide(boss, fireballs, True, pygame.sprite.collide_mask)):
        print "#boss is hit"
        boss.hit()
    if (pygame.sprite.groupcollide(fireballs, demons, True, True)):
        print "#fireball hit demon"
    if (pygame.sprite.groupcollide(fireballs, babies, True, True)):
        print "#fireball hit baby"
