import pygame
import random
from code.Entity import Bug, Obstacle

class Level:
    def __init__(self, window, clock):
        self.window = window
        self.clock = clock
        self.font = pygame.font.SysFont("Arial", 24)
        self.font_rodape = pygame.font.SysFont("Arial", 14)
        self.font_pause = pygame.font.SysFont("Arial", 48, bold=True)
        self.font_cause = pygame.font.SysFont("Arial", 30, bold=True)
        
        self.all_sprites = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        
        self.bug = Bug()
        self.all_sprites.add(self.bug)
        
        self.score = 0
        self.win_target = 10

        self.obstacle_speed = 5
        self.spawn_interval = 1500  # ms

        self.SPAWN_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.SPAWN_EVENT, self.spawn_interval)

        self._death_cause = ""
        self.paused = False

        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            pygame.mixer.music.load("asset/sounds/DOS-88 - City Stomper.mp3")
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(-1)

            self.bg_static = pygame.image.load("asset/images/10.png").convert_alpha()
            self.bg_static = pygame.transform.scale(self.bg_static, (800, 600))
            
            self.bg_layers = []
            self.scrolls = []
            self.speeds = []

            for i in range(1, 10):
                img = pygame.image.load(f"asset/images/{i}.png").convert_alpha()
                img = pygame.transform.scale(img, (800, 600))
                self.bg_layers.append(img)
                self.scrolls.append(0)
                self.speeds.append(i * 0.5)

        except Exception as e:
            print(f"Erro ao carregar as camadas de Parallax: {e}")
            self.bg_static = None

    def _update_difficulty(self):
        level = int(self.score) // 3
        new_speed = min(5 + level, 12)        
        new_interval = max(1500 - level * 100, 700)  

        if new_speed != self.obstacle_speed:
            self.obstacle_speed = new_speed

        if new_interval != self.spawn_interval:
            self.spawn_interval = new_interval
            pygame.time.set_timer(self.SPAWN_EVENT, self.spawn_interval)

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
            self.window.fill((135, 206, 235))

    def _draw_pause_overlay(self):
        overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.window.blit(overlay, (0, 0))
        pause_surf = self.font_pause.render("⏸  PAUSADO", True, (255, 255, 0))
        hint_surf = self.font.render("Pressione [ESC] para continuar", True, (200, 200, 200))
        self.window.blit(pause_surf, (pause_surf.get_rect(centerx=400, centery=270)))
        self.window.blit(hint_surf, (hint_surf.get_rect(centerx=400, centery=340)))

    def run(self):
        playing = True
        while playing:
            self.draw_parallax()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False, self.score, "saiu do jogo"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not self.paused:
                        self.bug.jump()
                    if event.key == pygame.K_ESCAPE:
                        self.paused = not self.paused
                if event.type == self.SPAWN_EVENT and not self.paused:
                    self.spawn_obstacle_pair()

            if self.paused:
                self._draw_pause_overlay()
                pygame.display.update()
                self.clock.tick(60)
                continue

            self.all_sprites.update()
            
            self._update_difficulty()

            for obs in self.obstacles:
                if not obs.passed and obs.rect.right < self.bug.rect.left:
                    obs.passed = True
                    self.score += 0.5

            for obs in list(self.obstacles):
                if obs.rect.right < 0:
                    obs.kill()

            # Colisão com obstáculo
            if pygame.sprite.spritecollide(self.bug, self.obstacles, False):
                return False, int(self.score), "colidiu com um obstáculo"

            # Saiu dos limites
            if self.bug.rect.bottom > 600:
                return False, int(self.score), "caiu para fora da tela"
            if self.bug.rect.top < 0:
                return False, int(self.score), "voou para fora da tela"

            if self.score >= self.win_target:
                return True, int(self.score), ""

            self.all_sprites.draw(self.window)
            
            # HUD de score
            score_surf = self.font.render(
                f"Bugs Desviados: {int(self.score)}/{self.win_target}  |  Vel: {self.obstacle_speed}",
                True, (255, 255, 255)
            )
            self.window.blit(score_surf, (10, 10))

            # Dica de pausa
            hint_surf = self.font_rodape.render("[ESC] Pausar", True, (180, 180, 180))
            self.window.blit(hint_surf, (10, 40))
            
            # Marca d'água
            creditos_surf = self.font_rodape.render("Dev: Rafael Barbosa | RU: 5255383", True, (200, 200, 200))
            self.window.blit(creditos_surf, (520, 575))

            pygame.display.update()
            self.clock.tick(60)

    def spawn_obstacle_pair(self):
        gap = 180
        top_height = random.randint(50, 350)
        bottom_height = 600 - (top_height + gap)
        
        # MELHORIA: passa a velocidade atual para o obstáculo
        top_obs = Obstacle(800, 0, is_top=True, height=top_height, speed=self.obstacle_speed)
        bottom_obs = Obstacle(800, 600, is_top=False, height=bottom_height, speed=self.obstacle_speed)
        
        self.all_sprites.add(top_obs, bottom_obs)
        self.obstacles.add(top_obs, bottom_obs)