import pygame
import sys
from code.Menu import Menu
from code.Level import Level

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.window = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Bug Jump")
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            menu = Menu(self.window)
            menu.run()
            level = Level(self.window, self.clock)
            vitoria, pontos, causa = level.run()
            menu.run_game_over(vitoria, pontos, causa)