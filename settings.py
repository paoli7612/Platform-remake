try:
    from gtk import gdk
    HEIGHT = gdk.screen_height() - 200
except:
    HEIGHT = 600
# game options/settings
TITLE = "Jumpy!"
WIDTH = 480
CENTERX = WIDTH/2
SIZE = (WIDTH,HEIGHT)

TOT_PLATFORMS = int(HEIGHT/100) - 1
FPS = 60
FONT_NAME = 'arial'
HS_FILE = "highscore.txt"
SPRITESHEET = "spritesheet_jumper.png"

# Player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8
PLAYER_JUMP = 20

# SUn properties
SUN_SPEED = 200
SUN_SIZE = int(WIDTH/3)

# Coins properties
COIN_SPEED = 100
COINS_VALUE = {"gold":5, "silver":2, "bronze":1}
COIN_SPAWN_PCT = 20
COINS_PCT = {"gold":10, "silver":30, "bronze":60}

# Game properties
BOOST_POWER = HEIGHT/12
POW_SPAWN_PCT = 7
DECOR_SPAWN_PCT = 50
MOB_FREQ = 5000
PLAYER_LAYER = 3
PLATFORM_LAYER = 2
POW_LAYER = 2
MOB_LAYER = 3
COIN_LAYER = 4
DECOR_LAYER = 1
CLOUD_LAYER = 0
SUN_LAYER = 0

# Starting platforms
from random import randrange
ZOOM_FACTOR = randrange(2,3)
PLATFORM_LIST = [(0, HEIGHT - 60)]
for p in range(TOT_PLATFORMS):
    PLATFORM_LIST += [(randrange(0,WIDTH-200),p*HEIGHT/TOT_PLATFORMS)]


PLATFORM_TYPES = ["grass","cake","sand","snow","wood","stone"]
# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
BGCOLOR = LIGHTBLUE
