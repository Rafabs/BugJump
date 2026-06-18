import pygame
import random
import os

class Bug(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            self.image = pygame.image.load("asset/images/bug.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (50, 50))
        except Exception as e:
            print(f"Erro ao carregar o sprite do Bug: {e}")
            self.image = pygame.Surface((50, 50))
            self.image.fill((255, 0, 0)) 
            
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 300
        self.gravity = 0.6
        self.speed_y = 0

    def update(self):
        self.speed_y += self.gravity
        self.rect.y += int(self.speed_y)

    def jump(self):
        self.speed_y = -9


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, is_top, height):
        super().__init__()
        
        # --- FILTRAGEM DINÂMICA DA PASTA DE IMAGENS ---
        pasta_imagens = "asset/images"
        lista_obstaculos = []
        
        # Lista de nomes de arquivos que NÃO devem ser usados como obstáculos
        arquivos_excluidos = ["bug.png", "Access_granted.png", "menu.png"]
        # Adiciona os fundos '1.png' até '10.png' na lista de exclusão
        for i in range(1, 11):
            arquivos_excluidos.append(f"{i}.png")
            
        try:
            # Varre todos os arquivos dentro da pasta asset/images
            for arquivo in os.listdir(pasta_imagens):
                # Se for uma imagem PNG e não estiver na lista de exclusão, vira obstáculo!
                if arquivo.lower().endswith('.png') and arquivo not in arquivos_excluidos:
                    lista_obstaculos.append(arquivo)
                    
            # Escolhe uma imagem aleatória dentre os obstáculos válidos encontrados
            if lista_obstaculos:
                img_nome = random.choice(lista_obstaculos)
            else:
                # Caso a pasta esteja vazia de obstáculos, define um nome padrão seguro
                img_nome = "cpuM6800.png"
                
            self.image = pygame.image.load(f"asset/images/{img_nome}").convert_alpha()
            self.image = pygame.transform.scale(self.image, (70, height))
            
        except Exception as e:
            print(f"Erro ao carregar obstáculo dinâmico: {e}")
            self.image = pygame.Surface((70, height))
            self.image.fill((0, 255, 0)) # Fallback seguro
        
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        
        if is_top:
            self.rect.top = y_pos
        else:
            self.rect.bottom = y_pos
            
        self.speed_x = 5
        self.passed = False

    def update(self):
        self.rect.x -= self.speed_x