import pygame
import random
from code.Entity import Bug, Obstacle

class Level:
    def __init__(self, window, clock):
        self.window = window
        self.clock = clock
        self.font = pygame.font.SysFont("Arial", 24)
        
        self.all_sprites = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        
        self.bug = Bug()
        self.all_sprites.add(self.bug)
        
        self.score = 0
        self.win_target = 10
        
        self.SPAWN_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.SPAWN_EVENT, 1500)

        # --- SISTEMA DE PARALLAX (Multi-camadas de 1.png a 9.png + estática 10.png) ---
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            # Carrega a música da PARTIDA diretamente da pasta asset/sounds
            pygame.mixer.music.load("asset/sounds/DOS-88 - City Stomper.mp3")
            pygame.mixer.music.set_volume(0.4) # Volume um pouco mais baixo para equilibrar com efeitos
            pygame.mixer.music.play(-1) # Toca em loop durante a partida            
            self.bg_static = pygame.image.load("asset/images/10.png").convert_alpha()
            self.bg_static = pygame.transform.scale(self.bg_static, (800, 600))
            
            # Listas para guardar as imagens e os controles de scroll de cada camada
            self.bg_layers = []
            self.scrolls = []
            self.speeds = []

            # Loop para carregar dinamicamente as imagens de 1 a 9
            for i in range(1, 9):
                img = pygame.image.load(f"asset/images/{i}.png").convert_alpha()
                img = pygame.transform.scale(img, (800, 600))
                self.bg_layers.append(img)
                self.scrolls.append(0)
                
                # Velocidade progressiva: a camada 1 se move a 0.5px/frame, a camada 9 a 4.5px/frame
                self.speeds.append(i * 0.5)

        except Exception as e:
            print(f"Erro ao carregar as 10 camadas de Parallax: {e}")
            self.bg_static = None

        # Controles de scroll para o Parallax
        self.scroll_l1 = 0
        self.scroll_l2 = 0

    def draw_parallax(self):
            if self.bg_static:
                self.window.blit(self.bg_static, (0, 0))
                for i in range(len(self.bg_layers)):
                    self.scrolls[i] -= self.speeds[i]
                    if abs(self.scrolls[i]) > 800:
                        self.scrolls[i] = 0
                    self.window.blit(self.bg_layers[i], (self.scrolls[i], 0))
                    self.window.blit(self.bg_layers[i], (self.scrolls[i] + 800, 0))
            else:
                self.window.fill((135, 206, 235)) # Fallback

    def run(self):
        playing = True
        while playing:
            self.draw_parallax()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False, self.score
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.bug.jump()
                if event.type == self.SPAWN_EVENT:
                    self.spawn_obstacle_pair()

            self.all_sprites.update()
            
            for obs in self.obstacles:
                if not obs.passed and obs.rect.right < self.bug.rect.left:
                    obs.passed = True
                    self.score += 0.5 

            if pygame.sprite.spritecollide(self.bug, self.obstacles, False):
                return False, int(self.score)
            
            if self.bug.rect.bottom > 600 or self.bug.rect.top < 0:
                return False, int(self.score)

            if self.score >= self.win_target:
                return True, int(self.score)

            self.all_sprites.draw(self.window)
            
            score_surf = self.font.render(f"Bugs Desviados: {int(self.score)}/{self.win_target}", True, (255, 255, 255))
            self.window.blit(score_surf, (10, 10))
            
            # --- MARCA D'ÁGUA DO ALUNO DENTRO DO JOGO ---
            font_rodape = pygame.font.SysFont("Arial", 14)
            creditos_surf = font_rodape.render("Dev: Rafael Barbosa | RU: 5255383", True, (200, 200, 200))
            # Posiciona no canto inferior direito (X=520, Y=575)
            self.window.blit(creditos_surf, (520, 575))

            pygame.display.update()
            self.clock.tick(60)

    def spawn_obstacle_pair(self):
        gap = 180
        top_height = random.randint(50, 350)
        bottom_height = 600 - (top_height + gap)
        
        top_obs = Obstacle(800, 0, is_top=True, height=top_height)
        bottom_obs = Obstacle(800, 600, is_top=False, height=bottom_height)
        
        self.all_sprites.add(top_obs, bottom_obs)
        self.obstacles.add(top_obs, bottom_obs)