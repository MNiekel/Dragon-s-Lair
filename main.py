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

TRANSPARENT = 0, 0, 255
BLACK = 0, 0, 0
WHITE = 255, 255, 255
YELLOW = 255, 255, 0
RED = 255, 0, 0
GREEN = 0, 255, 0

images = {'DRAGON' : 0, 'BOSS' : 0, 'FIREBALL' : 0, 'DEMON' : 0, 'BABY' : 0}

class Gamecontrol(object):

    def __init__(self):
        self.objects = []

    def init_screen(size):
        self.screen = pygame.display.set_mode(size)
        self.background 
        background = pygame.Surface(size)
        screen.blit(bg_image, [0, 0])
        return screen, bg_image

    def add_object(self, obj):
        self.objects.append(obj)
        num = len(self.objects)

    def draw_statistics(self, sprite):
        #health, score, lives
        pass

    def update(self):
        #update statistics and sprites
        pass

    def draw_screen(self):
        #draw sprites and statistics
        pass

    def eval_events(self):
        #get events and do something with it
        pass

    def load_images(file):
        img = pygame.image.load(file).convert()
        img.set_colorkey(TRANSPARENT)

        return img

    def init_images(self):
        #load images and put in a dictionary/list
        self.images = {}
        self.images['bg'] = load_image("resources/Background800x480.bmp")
        self.images['dragon'] = load_image("resources/Dragon.gif")
        self.images['boss'] = load_image("resources/Boss.gif")
        self.images['boss_hit'] = load_image("resources/Boss_Hit.gif")
        self.images['fireball'] = load_image("resources/Fireball.gif")
        self.images['demon'] = load_image("resources/Demon2.gif")
        self.images['baby'] = load_image("resources/Baby.gif")

    def load_music(filename):
        pygame.mixer.music.load("resources/Music.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        return pygame.mixer.music.load("resources/Music.mp3")

    def load_sounds(file):
        return pygame.mixer.Sound(filename)

    def init_sounds(self):
        #load music and sounds
        self.sounds = {}
        self.sounds['music'] = pygame.mixer.music.load("resources/Music.mp3")
        self.sounds['hit_boss'] = load_sounds("resources/Boss_Hit.wav")
        self.sounds['hit_baby'] = load_sounds("resources/Baby_Hit.wav")
        self.sounds['hit_demon'] = load_sounds("resources/Demon_Hit.wav")

def init_screen(size):
    screen = pygame.display.set_mode(size)
    bg_image = pygame.image.load("resources/Background800x480.bmp").convert()
    background = pygame.Surface(size)
    screen.blit(bg_image, [0, 0])

    return screen, bg_image

def init_images():
    dragon = pygame.image.load("resources/Dragon.gif").convert()
    boss = pygame.image.load("resources/Boss.gif").convert()
    boss_hit = pygame.image.load("resources/Boss_Hit.gif").convert()
    fireball = pygame.image.load("resources/Fireball.gif").convert()
    demon = pygame.image.load("resources/Demon2.gif").convert()
    baby = pygame.image.load("resources/Baby.gif").convert()

    dragon.set_colorkey(TRANSPARENT)
    boss.set_colorkey(TRANSPARENT)
    boss_hit.set_colorkey(TRANSPARENT)
    fireball.set_colorkey(TRANSPARENT)
    demon.set_colorkey(TRANSPARENT)
    baby.set_colorkey(TRANSPARENT)

    return dragon, boss, boss_hit, fireball, demon, baby

def init_sound():
    music = pygame.mixer.music.load("resources/Music.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    boss_hit = pygame.mixer.Sound("resources/Boss_Hit.wav")
    baby_hit = pygame.mixer.Sound("resources/Baby_Hit.wav")
    demon_hit = pygame.mixer.Sound("resources/Demon_Hit.wav")
    dragon_hit = pygame.mixer.Sound("resources/Dragon_Hit.wav")

    return boss_hit, baby_hit, demon_hit, dragon_hit

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

class Object(pygame.sprite.Sprite):
    def __init__(self, image, screen):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.mask = pygame.mask.from_surface(image)
        self.rect = self.image.get_rect()
        self.screen = screen
        self.screen_size = screen.get_size()

    def get_rect(self):
        return self.rect

class Boss(Object):
    def __init__(self, image, altimage, screen):
        Object.__init__(self, image, screen)

        self.rect.topright = (self.screen_size[0] - 4, 200)
        self.altimage = altimage
        self.direction = 1
        self.step = 8
        self.energy = 100
        self.flash = -1
        self.autoheal = 50 #heal every autoheal updates

        pygame.time.set_timer(DEMON_EVENT, random.randint(2500, 4500))
        pygame.time.set_timer(BABY_EVENT, random.randint(1500, 7500))

    def release_demon(self, spritelist, image, screen):
        pygame.time.set_timer(DEMON_EVENT, random.randint(2500, 4500))
        spritelist.add(Demon(image, self.rect, screen))

    def release_baby(self, spritelist, image, screen):
        pygame.time.set_timer(BABY_EVENT, random.randint(1500, 7500))
        spritelist.add(Baby(image, self.rect, screen))

    def change_colour(self):
        img = self.image
        self.image = self.altimage
        self.altimage = img

    def set_energy(self, d):
        self.energy = min(100, self.energy + d)

    def hit(self):
        self.energy = min(100, self.energy - 10)
        if self.energy <= 0:
            print "You defeated the Boss"
            pygame.event.post(pygame.event.Event(QUIT))
        self.change_colour()
        self.flash = 1

    def update(self):
        if self.flash == 0:
            self.change_colour()
            self.flash = -1
        elif self.flash > 0:
            self.flash -= 1

        if self.autoheal < 0:
            self.energy += 1
            self.autoheal = 50
        else:
            self.autoheal -= 1

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

class Healthbar(Object):
    def __init__(self, screen, rect): #rect is rectangle of Boss
        bar = pygame.Surface((100, 8)).convert()
        bar.set_colorkey(TRANSPARENT)

        Object.__init__(self, bar, screen)

        self.rect.left = rect.left
        self.rect.bottom = rect.bottom

    def move(self, rect, health):
        self.rect.left = rect.left
        self.rect.bottom = rect.bottom

        health = min(100, health)

        x = (255 * health)/50 - 255

        if (health > 50):
            col = 255 - x, 255, 0
        elif (health > 10):
            col = 255, 255 + x, 0
        else:
            col = RED
            
        self.image.fill(TRANSPARENT)
        self.image.fill(col, Rect(0, 0, health, 8))

class Dragon(Object):
    def __init__(self, image, screen):
        Object.__init__(self, image, screen)

        self.rect.topleft = (4, 200)
        self.step = 8
        self.timer = 0
        self.lives = 3
        self.score = 0

    def move(self, key):
        rect = self.rect

        if key == K_UP:
            if rect.top > self.step:
                rect.top -= self.step
        if key == K_DOWN:
            if rect.bottom < self.screen_size[1] - self.step:
                rect.top += self.step

        self.rect = rect

    def fire(self, image):
        if self.timer < pygame.time.get_ticks():
            self.timer = pygame.time.get_ticks() + 500
            return Fireball(image, self.screen, self.rect)
        else:
            return None

    def hit(self):
        self.lives -= 1
        if self.lives < 0:
            print "GAME OVER"
            pygame.event.post(pygame.event.Event(QUIT))

    def set_score(self, points):
        self.score += points
        self.score = max(0, self.score)

    def hit_by_demon(self):
        self.lives -= 1
        if self.lives < 0:
            print "GAME OVER"
            pygame.event.post(pygame.event.Event(QUIT))
        self.score = max(0, self.score - 10)

    def hit_baby(self):
        self.score = max(0, self.score - 20)

    def hit_demon(self):
        self.score += 5

    def caught_baby(self):
        self.score += 10

    def hit_boss(self):
        pass

class Fireball(Object):
    def __init__(self, image, screen, position):
        Object.__init__(self, image, screen)

        self.rect.left = position.right
        self.rect.top = position.top
        self.step = 12

    def update(self):
        self.rect.left += self.step
        if self.rect.left > self.screen_size[0]:
            self.kill()
            del self

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
boss_hit_snd, baby_hit_snd, demon_hit_snd, dragon_hit_snd = init_sound()
rendering = pygame.sprite.RenderUpdates()

dragon = Dragon(dragon_img, screen)
boss = Boss(boss_img, boss_hit_img, screen)

healthbar = Healthbar(screen, boss.rect)

rendering.add(dragon)
rendering.add(boss)
rendering.add(healthbar)

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
    healthbar.move(boss.rect, boss.energy)
    score.update(dragon.score)

    pygame.display.update(rendering.draw(screen))
    pygame.display.update(fireballs.draw(screen))
    pygame.display.update(demons.draw(screen))
    pygame.display.update(babies.draw(screen))
    screen.blit(background, [0, 0])
    screen.blit(score, [0, 0])

    if (pygame.sprite.spritecollide(dragon, demons, True, None)):
        print "#hit by demon"
        dragon.hit_by_demon()
        dragon_hit_snd.play()
    if (pygame.sprite.spritecollide(dragon, babies, True, None)):
        print "#caught baby"
        #dragon.set_score(15)
        dragon.caught_baby()
    if (pygame.sprite.spritecollide(boss, fireballs, True, pygame.sprite.collide_mask)):
        print "#hit boss"
        boss.hit()
        dragon.hit_boss()
        boss_hit_snd.play()
    if (pygame.sprite.groupcollide(fireballs, demons, True, True)):
        print "#hit demon"
        #dragon.set_score(10)
        dragon.hit_demon()
        demon_hit_snd.play()
    if (pygame.sprite.groupcollide(fireballs, babies, True, True)):
        print "#hit baby"
        #dragon.set_score(-15)
        dragon.hit_baby()
        baby_hit_snd.play()
