import pygame
import sys

class Menu:
    def __init__(self, window):
        self.window = window
        # Fontes com hierarquia para o trabalho acadêmico
        self.font_title = pygame.font.SysFont("Arial", 40, bold=True)
        self.font_subtitle = pygame.font.SysFont("Arial", 22, bold=True)
        self.font_text = pygame.font.SysFont("Arial", 24)
        self.font_info = pygame.font.SysFont("Arial", 18, bold=True)
        
        # Cores temáticas (Verde Matrix de TI para dar destaque sobre a imagem)
        self.C_VERDE = (0, 255, 0)
        self.C_BRANCO = (255, 255, 255)
        self.C_CINZA = (180, 180, 180)
        self.C_VERMELHO = (255, 0, 0)
        
        # --- CARREGAMENTO DA SUA NOVA IMAGEM DE FUNDO ---
        try:
            self.bg_menu = pygame.image.load("asset/images/menu.png").convert_alpha()
            self.bg_menu = pygame.transform.scale(self.bg_menu, (800, 600))
            if not pygame.mixer.get_init():
                pygame.mixer.init()                        
            pygame.mixer.music.load("asset/sounds/DOS-88 - Automatav2.mp3") 
            pygame.mixer.music.set_volume(0.5) # Volume em 50%
            pygame.mixer.music.play(-1) # Toca em loop infinito            
        except Exception as e:
            print(f"Erro ao carregar asset/images/menu.png: {e}")
            print(f"Aviso: Não foi possível tocar a música do menu: {e}")            
            # Fallback caso dê algum problema com o nome do arquivo
            self.bg_menu = None

        try:
            self.img_granted = pygame.image.load("asset/images/Access_granted.png").convert_alpha()
            self.img_granted = pygame.transform.scale(self.img_granted, (200, 200))
        except:
            self.img_granted = None

    def run(self):
        while True:
            # 1. Desenha o seu fundo customizado do Bug Jump
            if self.bg_menu:
                self.window.blit(self.bg_menu, (0, 0))
                
                # Película escura semi-transparente para que seus dados e os comandos 
                # fiquem perfeitamente visíveis e legíveis por cima da arte
                filtro = pygame.Surface((800, 600), pygame.SRCALPHA)
                filtro.fill((10, 10, 10, 140)) # 140 é o nível de opacidade da sombra
                self.window.blit(filtro, (0, 0))
            else:
                self.window.fill((10, 10, 10))
            
            # --- RENDERIZAÇÃO DOS TEXTOS ACADÊMICOS E DE COMANDO ---
            title_surf = self.font_title.render("<> BUG JUMP </>", True, self.C_VERMELHO)
            
            # Suas informações de estudante bem destacadas no menu principal
            aluno_surf = self.font_info.render("Desenvolvido por: Rafael Barbosa", True, self.C_BRANCO)
            ru_surf = self.font_info.render("RU: 5255383", True, self.C_BRANCO)
            
            # Instruções e Controles (Item obrigatório do edital)
            cmd_title = self.font_subtitle.render("CONTROLES DO SISTEMA:", True, self.C_VERDE)
            cmd_text = self.font_text.render("[ESPAÇO] - Pular / Voar sobre os Erros", True, self.C_BRANCO)
            
            start_text = self.font_text.render("Pressione [ESPAÇO] para iniciar a depuração", True, self.C_CINZA)
            
            # --- POSICIONAMENTO DOS ELEMENTOS NA TELA (800x600) ---
            self.window.blit(title_surf, (240, 80))
            
            # Blit da sua identificação logo abaixo do título principal
            self.window.blit(aluno_surf, (255, 160))
            self.window.blit(ru_surf, (350, 190))
            
            # Caixa de comandos do jogo
            self.window.blit(cmd_title, (280, 290))
            self.window.blit(cmd_text, (220, 330))
            
            # Chamada para ação no rodapé
            self.window.blit(start_text, (190, 480))
            
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.img_granted:
                            self.window.fill((10, 10, 10))
                            self.window.blit(self.img_granted, (300, 200))
                            pygame.display.update()
                            pygame.time.delay(800)
                        return

    def run_game_over(self, vitoria, pontos):
        while True:
            self.window.fill((10, 10, 10))
            
            if vitoria:
                txt = self.font_title.render("COMPILAÇÃO REALIZADA!", True, self.C_VERDE)
                pos_x = 120
            else:
                txt = self.font_title.render("CRITICAL ERROR: GAME OVER", True, self.C_VERMELHO)
                pos_x = 80
                
            score_txt = self.font_text.render(f"Bugs corrigidos com sucesso: {pontos}", True, self.C_BRANCO)
            restart_txt = self.font_text.render("Pressione [R] para Reiniciar ou [Q] para Sair", True, self.C_CINZA)
            
            self.window.blit(txt, (pos_x, 180))
            self.window.blit(score_txt, (240, 280))
            self.window.blit(restart_txt, (190, 400))
            
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()