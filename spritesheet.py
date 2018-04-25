import pygame
from settings import *

class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pygame.image.load(filename).convert()
        self.images = Images(self)

    def get_image(self, x, y, width, height, zoom = ZOOM_FACTOR):
        # grab an image out of a larger spritesheet
        image = pygame.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pygame.transform.scale(image, (width // zoom, height // zoom))
        image.set_colorkey((0,0,0))
        return image

class Images:
    def __init__(self,spritesheet):
        self.get_image = spritesheet.get_image
        self.load_platforms()
        self.load_bunny()
        self.load_coin()
        self.load_powerups()
        self.load_decors()
        self.load_icons()
        self.load_suns()

    def load_icons(self):
        self.life = self.get_image(868,1936,52,71,2)
        bronze = self.get_image(329,1390,60,61,2)
        silver = self.get_image(307,1981,61,61,2)
        gold = self.get_image(244,1981,61,61,2)
        self.money = pygame.Surface((90,61))
        self.money.blit(gold,(0,0))
        self.money.blit(silver,(15,0))
        self.money.blit(bronze,(30,0))
        self.money.set_colorkey((0,0,0))

    def load_suns(self):
        self.sun = [self.get_image(534,913,142,148,1),
            self.get_image(421,1390,148,142,1)]

    def load_decors(self):
        self.decors = {"sand": self.get_image(707,134,117,160),
                        "grass": self.get_image(784,1931,82,70),
                        "wood": self.get_image(814,1574,81,85)}

    def load_powerups(self):
        self.powerup = {"boost": self.get_image(820,1805,71,70),
                        "life": self.get_image(826,1220,71,70)}

    def load_coin(self):
        self.coin = {"bronze":[self.get_image(707, 296, 84, 84),
                    self.get_image(826, 206, 66, 84),
                    self.get_image(899, 116, 50, 84),
                    self.get_image(670, 406, 14, 84),
                    pygame.transform.flip(self.get_image(899, 116, 50, 84), True, False),
                    pygame.transform.flip(self.get_image(826, 206, 66, 84), True, False)],
                    "silver":[self.get_image(584, 406, 84, 84),
                    self.get_image(852, 1003, 66, 84),
                    self.get_image(899, 1219, 50, 84),
                    self.get_image(662, 651, 14, 84),
                    pygame.transform.flip(self.get_image(852, 1003, 66, 84), True, False),
                    pygame.transform.flip(self.get_image(899, 1219, 50, 84), True, False)],
                    "gold":[self.get_image(698, 1931, 84, 84),
                    self.get_image(829, 0, 66, 84),
                    self.get_image(897, 1574, 50, 84),
                    self.get_image(645, 651, 15, 84),
                    pygame.transform.flip(self.get_image(829, 0, 66, 84), True, False),
                    pygame.transform.flip(self.get_image(897, 1574, 50, 84), True, False)]}

    def load_platforms(self):
        self.platforms = {"grass":[self.get_image(0, 288, 380, 94),
                        self.get_image(213, 1662, 201, 100)],
                        "cake":[self.get_image(0, 576, 380, 94),
                        self.get_image(218, 1456, 201, 100)],
                        "sand":[self.get_image(0, 672, 380, 94),
                        self.get_image(208, 1879, 201, 100)],
                        "snow":[self.get_image(0, 768, 380, 94),
                        self.get_image(213, 1764, 201, 100)],
                        "stone":[self.get_image(0, 96, 380, 94),
                        self.get_image(382, 408, 200, 100)],
                        "wood":[self.get_image(0, 960, 380, 94),
                        self.get_image(218, 1558, 200, 100)]}

    def load_bunny(self):
        class Bunny(object):
            standing = [self.get_image(614, 1063, 120, 191),
                        self.get_image(690, 406, 120, 201)]
            walking_r = [self.get_image(678, 860, 120, 201),
                        self.get_image(692, 1458, 120, 207)]
            walking_l = [pygame.transform.flip(walking_r[0], True, False),
                        pygame.transform.flip(walking_r[1], True, False)]
            jumping = self.get_image(382, 763, 150, 181)
            falling = self.get_image(382, 946, 150, 174)
        class Bunny_female(object):
            standing = [self.get_image(581, 1265, 121, 191),
                        self.get_image(584, 0, 121, 201)]
            walking_r = [self.get_image(584, 203, 121, 201),
                        self.get_image(678, 651, 121, 207)]
            walking_l = [pygame.transform.flip(walking_r[0], True, False),
                        pygame.transform.flip(walking_r[1], True, False)]
            jumping = self.get_image(416, 1660, 150, 181)
            falling = self.get_image(411, 1866, 150, 174)
        self.rabbits = [Bunny(),Bunny_female()]
