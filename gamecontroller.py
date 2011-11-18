class GameController(object):
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
        #self.sounds['caught_baby']
        #self.sounds['hit_by_demon']
