import pygame, time
import xml.etree.ElementTree as et
from spritesheet import Spritesheet

xml_path = "img/spritesheet_jumper.xml"
png_path = "img/spritesheet_jumper.png"

tree = et.parse(xml_path)
root = tree.getroot()
pygame.init()
screen = pygame.display.set_mode((400,400))
pygame.display.set_caption("spritesheet test")
clock = pygame.time.Clock()
font_name = pygame.font.match_font("arial")
font = pygame.font.Font(font_name, 20)
spritesheet = Spritesheet(png_path)

images = list()

for element in root:
    d = element.attrib
    name = d["name"].split(".")[0]
    name = name.replace("_", " ")
    coord = (d["x"],d["y"],d["width"],d["height"],1)
    coord = map(int,coord)
    surface = spritesheet.get_image(*coord)
    images += [(name,coord,surface)]

running = True
frame = 0
right,left = False,False
while running:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT: right = True
            if event.key == pygame.K_LEFT: left = True
            if event.key == pygame.K_d: frame = (frame+1)%len(images)
            if event.key == pygame.K_a: frame = (frame-1)%len(images)
            if event.key == pygame.K_SPACE: print(name,tuple(coord))
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT: right = False
            if event.key == pygame.K_LEFT: left = False
    if right: frame = (frame+1)%len(images)
    elif left: frame = (frame-1)%len(images)
    screen.fill((200,200,200))
    name,coord,image = images[frame]
    rect = image.get_rect()
    rect.center = 200,200
    screen.blit(image,rect)
    text_surface = font.render(name, True, (0,0,0))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (200, 350)
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
