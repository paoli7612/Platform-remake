# Sprite classes for platform game
import pygame
from settings import *
from random import choice, randrange
vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.life = 0
        self.images = choice(self.game.spritesheet.images.rabbits)
        self.image = self.images.standing[0]
        self.rect = self.image.get_rect()
        self.rect.center = (40, HEIGHT - 100)
        self.pos = vec(40, HEIGHT - 100)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.alive = True

    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def jump(self):
        # jump only if standing on a platform
        self.rect.y += 2
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 2
        if hits and not self.jumping:
            self.game.jump_sound.play()
            self.jumping = True
            self.vel.y = -PLAYER_JUMP

    def die(self):
        self.alive = False
        self.image = self.images.falling
        self.game.all_platforms = pygame.sprite.Group()

    def update(self):
        self.acc = vec(0, PLAYER_GRAV)
        if self.alive:
            self.animate()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.acc.x = -PLAYER_ACC
            if keys[pygame.K_RIGHT]:
                self.acc.x = PLAYER_ACC

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        # wrap around the sides of the screen
        if self.pos.x > WIDTH + self.rect.width / 2:
            self.pos.x = 0 - self.rect.width / 2
        if self.pos.x < 0 - self.rect.width / 2:
            self.pos.x = WIDTH + self.rect.width / 2

        self.rect.midbottom = self.pos

    def animate(self):
        now = pygame.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        # show walk animation
        if self.walking:
            if now - self.last_update > 180:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.images.walking_l)
                bottom = self.rect.bottom
                if self.vel.x > 0: self.image = self.images.walking_r[self.current_frame]
                else: self.image = self.images.walking_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        # show idle animation
        if not self.jumping and not self.walking:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.images.standing)
                bottom = self.rect.bottom
                self.image = self.images.standing[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        self.mask = pygame.mask.from_surface(self.image)

class Cloud(pygame.sprite.Sprite):
    def __init__(self, game):
        self._layer = CLOUD_LAYER
        self.groups = game.all_sprites, game.clouds
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = choice(self.game.cloud_images)
        self.rect = self.image.get_rect()
        scale = randrange(50, 101) / 100
        self.image = pygame.transform.scale(self.image, (int(self.rect.width * scale),
                                                     int(self.rect.height * scale)))
        self.rect.x = randrange(WIDTH - self.rect.width)
        self.rect.y = randrange(-500, -50)

    def update(self):
        if self.rect.top > HEIGHT * 2:
            self.kill()

class Platform(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLATFORM_LAYER
        self.groups = game.all_sprites, game.platforms
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.type = choice(PLATFORM_TYPES)
        images = self.game.spritesheet.images.platforms[self.type]
        self.image = choice(images)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        prob = randrange(100)
        if prob < POW_SPAWN_PCT: Pow(self.game, self)
        elif prob < COIN_SPAWN_PCT: Coin(self.game, self)
        if prob < DECOR_SPAWN_PCT: Decor(game,self)

class Pow(pygame.sprite.Sprite):
    def __init__(self, game, plat):
        self._layer = POW_LAYER
        self.groups = game.all_sprites, game.powerups
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        self.type = choice(['boost','life'])
        self.image = self.game.spritesheet.images.powerup[self.type]
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5

    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        if not self.game.platforms.has(self.plat):
            self.kill()

class Mob(pygame.sprite.Sprite):
    def __init__(self, game):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image_up = self.game.spritesheet.get_image(566, 510, 122, 139)
        self.image_down = self.game.spritesheet.get_image(568, 1534, 122, 135)
        self.image = self.image_up
        self.rect = self.image.get_rect()
        self.rect.centerx = choice([-100, WIDTH + 100])
        self.vx = randrange(1, 4)
        if self.rect.centerx > WIDTH:
            self.vx *= -1
        self.rect.y = randrange(HEIGHT / 2)
        self.vy = 0
        self.dy = 0.5

    def update(self):
        self.rect.x += self.vx
        self.vy += self.dy
        if self.vy > 3 or self.vy < -3: self.dy *= -1
        center = self.rect.center
        if self.dy < 0: self.image = self.image_up
        else: self.image = self.image_down
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = center
        self.rect.y += self.vy
        if self.rect.left > WIDTH + 100 or self.rect.right < -100: self.kill()

class Coin(pygame.sprite.Sprite):
    def __init__(self, game, plat):
        self._layer = COIN_LAYER
        self.groups = game.all_sprites, game.coins
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        types = list(self.game.spritesheet.images.coin.keys())
        prob = randrange(100)
        for k in COINS_PCT:
            if prob <= COINS_PCT[k]: self.type = k; break
        self.type = choice(types)
        self.value = COINS_VALUE[self.type]
        self.images = self.game.spritesheet.images.coin[self.type]
        self.current_frame = 0
        self.last_update = 0
        self.image = self.images[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5

    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        if not self.game.platforms.has(self.plat):self.kill()
        now = pygame.time.get_ticks()
        if now - self.last_update > COIN_SPEED:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.images)
            x = self.rect.centerx
            self.image = self.images[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = self.plat.rect.top - 5
            self.rect.centerx = x

class Sun(pygame.sprite.Sprite):
    def __init__(self, game):
        self._layer = SUN_LAYER
        self.game = game
        pygame.sprite.Sprite.__init__(self, game.all_sprites)
        self.images = self.game.spritesheet.images.sun
        self.current_frame = 0
        self.image = self.images[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = 100,100
        self.last_update = 0

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > SUN_SPEED:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.image = self.images[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.center = 100,100

class Decor(pygame.sprite.Sprite):
    def __init__(self, game, plat):
        self._layer = DECOR_LAYER
        pygame.sprite.Sprite.__init__(self, game.all_sprites)
        self.game = game
        self.plat = plat
        self.type = self.plat.type
        if not self.type in self.game.spritesheet.images.decors:
            self.kill(); return
        self.image = self.game.spritesheet.images.decors[self.type]
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5

    def update(self):
        self.rect.bottom = self.plat.rect.top
        if not self.game.platforms.has(self.plat): self.kill()
