import pygame
from settings import *

class Writer:
    def __init__(self,game):
        self.game = game
        self.font_name = pygame.font.match_font(FONT_NAME)
        self.font_title = pygame.font.Font(self.font_name, 48)
        self.font_text = pygame.font.Font(self.font_name, 22)
        self.set_loading_screen()

    def change_score(self):
        self.set_go_screen(self.game.highscore,self.game.score)

    def set_loading_screen(self):
        self.loading_screen = pygame.Surface(SIZE)
        self.loading_screen.fill(BGCOLOR)
        self.draw_text(self.loading_screen, TITLE, HEIGHT/4)
        self.draw_text(self.loading_screen, "Loading", HEIGHT / 2)

    def set_start_screen(self):
        self.start_screen = pygame.Surface(SIZE)
        self.start_screen.fill(BGCOLOR)
        self.draw_text(self.start_screen,TITLE, HEIGHT / 4)
        self.draw_text(self.start_screen,"Arrows to move, Space to jump", HEIGHT / 2)
        self.draw_text(self.start_screen,"Press a key to play", HEIGHT * 3 / 4)
        self.draw_text(self.start_screen,"High Score: " + str(self.game.highscore), 15)

    def set_go_screen(self, highscore, score):
        self.go_screen = pygame.Surface(SIZE)
        self.go_screen.fill(BGCOLOR)
        self.draw_text(self.go_screen,"GAME OVER", HEIGHT / 4)
        self.draw_text(self.go_screen,"Score: " + str(score), HEIGHT / 2)
        self.draw_text(self.go_screen,"Press a key to play again", HEIGHT * 3 / 4)
        if score > highscore:
            self.draw_text(self.go_screen,"NEW HIGH SCORE!", HEIGHT / 2 + 40)
        else:
            self.draw_text(self.go_screen,"High Score: " + str(highscore), HEIGHT / 2 + 40)

    def draw_text(self, surface, text, y, x=CENTERX):
        if text == TITLE: font = self.font_title
        else: font = self.font_text
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surface.blit(text_surface, text_rect)
