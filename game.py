import pygame
import random
import os
from settings import *
from player import Player
from platform import Platform

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.SysFont("arial", 22, bold=True)
        self.font_large = pygame.font.SysFont("arial", 36, bold=True) # Fonte para o "Aperte Espaço"
        self.load_audio()
        self.load_data() # Puxa o recorde salvo ao iniciar o jogo

    # Agora a função está alinhada corretamente (fora do __init__)
    def load_data(self):
        # Tenta abrir o arquivo. Se não existir (ex: na primeira vez ou se apagar), o recorde é 0.
        try:
            with open(HS_FILE, 'r') as f:
                self.highscore = int(f.read())
        except:
            self.highscore = 0
        
    def load_audio(self):
        pygame.mixer.init()
        self.sounds = {}
        for snd in ['jump.wav', 'gameover.wav', 'platform_break.wav']:
            try:
                self.sounds[snd] = pygame.mixer.Sound(os.path.join('assets', 'sounds', snd))
            except:
                self.sounds[snd] = None
        try:
            pygame.mixer.music.load(os.path.join('assets', 'music', 'gameplay_music.mp3'))
        except:
            pass

    def play_sound(self, name):
        if self.sounds.get(name):
            self.sounds[name].play()

    def new(self):
        self.score = 0
        self.game_started = False # Jogo começa "pausado" no chão
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)

        # 1. Cria o Chão Fixo (ocupando toda a largura da tela)
        self.ground = Platform(0, HEIGHT - 40, "static", WIDTH, 40)
        self.all_sprites.add(self.ground)
        self.platforms.add(self.ground)

        # Posiciona o jogador exatamente em cima do chão
        self.player.pos.y = self.ground.rect.top
        self.player.vel.y = 0

        # 2. Gera as plataformas baseadas no Y da última plataforma
        highest_y = self.ground.rect.top
        for i in range(8):
            # A próxima plataforma fica entre 70 e 110 pixels acima da anterior
            new_y = highest_y - random.randint(70, 110)
            self.spawn_platform(new_y)
            highest_y = new_y # Atualiza para o próximo loop
            
        if pygame.mixer.music.get_busy() == False:
            try: pygame.mixer.music.play(loops=-1)
            except: pass
            
        self.run()

    def spawn_platform(self, y_pos):
        x_pos = random.randint(0, WIDTH - PLATFORM_WIDTH)
        p_type = random.choices(["static", "moving", "breaking"], weights=[70, 20, 10])[0]
        
        # Passamos o self.score no final para a plataforma saber a pontuação atual
        p = Platform(x_pos, y_pos, p_type, PLATFORM_WIDTH, PLATFORM_HEIGHT, self.score)
        
        self.all_sprites.add(p)
        self.platforms.add(p)

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.all_sprites.update()

        # Se o jogo ainda não começou, mantém o jogador colado no chão
        if not self.game_started:
            self.player.pos.y = self.ground.rect.top
            self.player.vel.y = 0
            self.player.rect.midbottom = self.player.pos
            return 

        # Colisão com plataforma (apenas caindo)
        if self.player.vel.y > 0:
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest_hit = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest_hit.rect.bottom:
                        lowest_hit = hit
                        
                # Garante a colisão mesmo se o personagem cair muito rápido ou acertar a quina.
                if self.player.pos.y <= lowest_hit.rect.bottom:
                    self.player.pos.y = lowest_hit.rect.top
                    self.player.vel.y = 0
                    self.player.jump()
                    self.play_sound('jump.wav')
                    
                    if lowest_hit.type == "breaking":
                        lowest_hit.kill()
                        self.play_sound('platform_break.wav')

        # Câmera: Se o jogador for para a metade superior da tela
        if self.player.rect.top <= HEIGHT / 2:
            self.player.pos.y += abs(self.player.vel.y)
            for plat in self.platforms:
                plat.rect.y += abs(self.player.vel.y)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10
                    
        # Gera novas plataformas: sempre baseadas na que estiver mais alta no momento
        while len(self.platforms) < 8:
            if len(self.platforms) > 0:
                highest_y = min([p.rect.y for p in self.platforms])
            else:
                highest_y = HEIGHT / 2

            new_y = highest_y - random.randint(70, 110)
            self.spawn_platform(new_y)

        # Game Over: Se cair pelo fundo da tela
        if self.player.rect.bottom > HEIGHT:
            self.playing = False
            self.play_sound('gameover.wav')
            pygame.mixer.music.stop()
            
            # --- PARTE QUE FALTAVA: SALVAR O RECORDE NO ARQUIVO ---
            if self.score > self.highscore:
                self.highscore = self.score
                with open(HS_FILE, 'w') as f:
                    f.write(str(self.score))

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.playing = False
                    self.running = False
                # Ao apertar ESPAÇO, se o jogo não tiver começado, ele começa e pula!
                if event.key == pygame.K_SPACE and not self.game_started:
                    self.game_started = True
                    self.player.jump()
                    self.play_sound('jump.wav')

    def draw(self):
        try:
            bg = pygame.image.load(os.path.join('assets', 'sprites', 'background.png')).convert()
            self.screen.blit(bg, (0, 0))
        except:
            self.screen.fill(DARK_GREY)
            
        self.all_sprites.draw(self.screen)
        
        # Texto piscante "APERTE ESPAÇO" enquanto o jogo não começa
        if not self.game_started:
            text_obj = self.font_large.render("APERTE ESPAÇO", True, WHITE)
            text_rect = text_obj.get_rect(center=(WIDTH/2, HEIGHT/2 - 50))
            self.screen.blit(text_obj, text_rect)
        
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        pygame.display.flip()