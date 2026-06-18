import pygame
import sys
from code.Menu import Menu
from code.Level import Level

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()     
        pygame.mixer.music.load("asset/sounds/DOS-88 - Automatav2.mp3")  # Carrega a música usando o caminho relativo correto    
        pygame.mixer.music.set_volume(0.3)  # Define o volume (de 0.0 a 1.0)        
        pygame.mixer.music.play(-1) # Toca a música. O argumento -1 faz ela tocar em loop infinito
        self.window = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Bug Jump")
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            # 1. Abre o Menu
            menu = Menu(self.window)
            menu.run()
            
            # 2. Quando sai do menu, inicia a fase (Level)
            level = Level(self.window, self.clock)
            vitoria, pontos = level.run()
            
            # 3. Mostra a tela de encerramento baseada no resultado
            menu.run_game_over(vitoria, pontos)