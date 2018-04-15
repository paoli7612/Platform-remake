import pygame,random,os
from spritesheet import *
from settings import *
from sprites import *
from writer import Writer


class Game:
    def __init__(self):
        # initialize game window, etc
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode(SIZE)
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.writer = Writer(self)
        self.show_loading_screen()
        self.load_data()
        self.writer.set_start_screen()

    def load_data(self):
        # load high score
        self.dir = os.path.dirname(__file__)
        if HS_FILE in os.listdir(os.getcwd()):
            with open(os.path.join(self.dir, HS_FILE), 'r') as f:
                try:
                    hm = f.read().split("-")
                    self.highscore = int(hm[0])
                    self.money = int(hm[1])
                except: self.highscore = 0
        else: open(os.path.join(self.dir, HS_FILE), 'w'); self.highscore = 0; self.money = 0
        # load spritesheet image
        img_dir = os.path.join(self.dir, 'img')
        self.spritesheet = Spritesheet(os.path.join(img_dir, SPRITESHEET))
        # cloud images
        self.cloud_images = []
        for i in range(1, 4):
            img = pygame.image.load(os.path.join(img_dir, 'cloud{}.png'.format(i))).convert()
            img.set_colorkey(BLACK)
            self.cloud_images.append(img)
        # load sounds
        self.snd_dir = os.path.join(self.dir, 'snd')
        self.jump_sound = pygame.mixer.Sound(os.path.join(self.snd_dir, 'Jump33.wav'))
        self.boost_sound = pygame.mixer.Sound(os.path.join(self.snd_dir, 'Boost16.wav'))

    def new(self):
        # start a new game
        self.score = 0
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.platforms = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.clouds = pygame.sprite.Group()
        self.player = Player(self)
        for plat in PLATFORM_LIST:
            Platform(self, *plat)
        self.mob_timer = 0
        pygame.mixer.music.load(os.path.join(self.snd_dir, 'Happy Tune.ogg'))
        for i in range(8):
            c = Cloud(self)
            c.rect.y += 500
        self.run()

    def run(self):
        # Game Loop
        pygame.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pygame.mixer.music.fadeout(500)

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()

        # spawn a mob?
        now = pygame.time.get_ticks()
        if now - self.mob_timer > 5000 + random.choice([-1000, -500, 0, 500, 1000]):
            self.mob_timer = now
            Mob(self)
        # hit mobs?

        mob_hits = pygame.sprite.spritecollide(self.player, self.mobs, True)
        for mob in mob_hits:
            if self.player.life > 0:
                self.player.life -= 1
                mob.kill()
            else:
                self.player.die()

        # check if player hits a platform - only if falling
        if self.player.vel.y > 0 and self.player.alive:
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.player.pos.x < lowest.rect.right + 10 and \
                   self.player.pos.x > lowest.rect.left - 10:
                    if self.player.pos.y < lowest.rect.centery:
                        self.player.pos.y = lowest.rect.top
                        self.player.vel.y = 0
                        self.player.jumping = False

        # if player reaches top 1/4 of screen
        if self.player.rect.top <= HEIGHT / 4:
            if random.randrange(100) < 15:
                Cloud(self)
            self.player.pos.y += max(abs(self.player.vel.y), 2)
            for cloud in self.clouds:
                cloud.rect.y += max(abs(self.player.vel.y / 2), 2)
            for mob in self.mobs:
                mob.rect.y += max(abs(self.player.vel.y), 2)
            for plat in self.platforms:
                plat.rect.y += max(abs(self.player.vel.y), 2)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10

        # if player hits powerup
        pow_hits = pygame.sprite.spritecollide(self.player, self.powerups, True)
        for pow in pow_hits:
            if pow.type == 'boost':
                self.boost_sound.play()
                self.player.vel.y = -BOOST_POWER
                self.player.jumping = False
            if pow.type == 'life':
                self.player.life += 1
                pow.kill()

        # if player hits coin
        coin_hits = pygame.sprite.spritecollide(self.player, self.coins, True)
        for coin in coin_hits:
            coin.kill()
            self.money += coin.value

        # Die!
        if self.player.rect.bottom > HEIGHT:
            if self.player.life > 0:
                self.player.life -= 1
                self.player.vel.y = -HEIGHT/20
                self.player.jumping = False
            else:
                for sprite in self.all_sprites:
                    sprite.rect.y -= max(self.player.vel.y, 10)
                    if sprite.rect.bottom < 0:
                        sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False

        # spawn new platforms to keep same average number
        while len(self.platforms) < TOT_PLATFORMS:
            width = random.randrange(50, 100)
            Platform(self, random.randrange(0, WIDTH - width),
                     random.randrange(-50, -40))

    def events(self):
        # Game Loop - events
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.player.jump_cut()

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.writer.draw_text(self.screen,str(self.score), 15)
        for sy in range(self.player.life):
            self.screen.blit(self.spritesheet.images.life,(2 + 30*sy,10))
        self.screen.blit(self.spritesheet.images.money,(WIDTH - 110,10))
        self.writer.draw_text(self.screen, str(self.money), 15, WIDTH-30)
        pygame.display.flip()

    def show_start_screen(self):
        pygame.mixer.music.load(os.path.join(self.snd_dir, 'Yippee.ogg'))
        pygame.mixer.music.play(loops=-1)
        self.screen.blit(self.writer.start_screen,(0,0))
        pygame.display.flip()
        self.wait_for_key()
        pygame.mixer.music.fadeout(500)

    def show_go_screen(self):
        if not self.running: return
        pygame.mixer.music.load(os.path.join(self.snd_dir, 'Yippee.ogg'))
        pygame.mixer.music.play(loops=-1)
        self.writer.change_score()
        self.screen.blit(self.writer.go_screen,(0,0))
        pygame.display.flip()
        self.save_data()
        self.wait_for_key()
        pygame.mixer.music.fadeout(500)

    def show_loading_screen(self):
        self.screen.blit(self.writer.loading_screen,(0,0))
        pygame.display.flip()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    waiting = False

    def save_data(self):
        f = open(os.path.join(self.dir, HS_FILE), 'w')
        f.write(str(self.highscore) + "-" + str(self.money))
        f.close()

def main():
    g = Game()
    g.show_start_screen()
    while g.running:
        g.new()
        g.show_go_screen()
    pygame.quit()


if __name__ == "__main__":
    main()
