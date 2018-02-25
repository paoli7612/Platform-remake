import pygame

class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pygame.image.load(filename).convert()
        self.images = Images(self)

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pygame.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pygame.transform.scale(image, (width // 2, height // 2))
        image.set_colorkey((0,0,0))
        return image

class Images:
    def __init__(self,spritesheet):
        self.get_image = spritesheet.get_image
        self.load_platforms()
        self.load_bunny()
        self.coin = self.get_image(707, 296, 84, 84)

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
        class Frames(object):
            standing = [self.get_image(614, 1063, 120, 191),
                        self.get_image(690, 406, 120, 201)]
            walking_r = [self.get_image(678, 860, 120, 201),
                        self.get_image(692, 1458, 120, 207)]
            walking_l = [pygame.transform.flip(walking_r[0], True, False),
                        pygame.transform.flip(walking_r[1], True, False)]
            jumping = self.get_image(382, 763, 150, 181)
        self.bunny = Frames
