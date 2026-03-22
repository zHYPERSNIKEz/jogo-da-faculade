import pygame
import random
import os
import json
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
        self.font_large = pygame.font.SysFont("arial", 32, bold=True)
        
        # Configurações iniciais
        self.config = {
            'lang': 'pt',
            'master': 10,
            'music': 10,
            'sfx': 10
        }
        self.current_music = None
        
        self.load_audio()
        self.load_data()
        
        # Carrega o background
        try:
            bg_img = pygame.image.load(os.path.join('assents', 'sprites', 'background.png')).convert()
            self.bg = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
        except:
            self.bg = None

    def play_music(self, track_name):
        self.current_music = track_name
        self.update_music_volume()
        if self.config['master'] and self.config['music']:
            if not pygame.mixer.music.get_busy():
                try:
                    pygame.mixer.music.load(os.path.join('assents', 'music', track_name))
                    pygame.mixer.music.play(-1)
                except: pass

    def load_data(self):
        # Carrega o recorde
        try:
            with open(HS_FILE, 'r') as f:
                self.highscore = int(f.read())
        except:
            self.highscore = 0
            
        # Carrega as configurações de áudio e idioma
        try:
            with open(CONFIG_FILE, 'r') as f:
                self.config = json.load(f)
        except:
            self.config = {
                'lang': 'pt',
                'mute': False,
                'master': 10,
                'music': 10,
                'sfx': 10
            }

    def save_config(self):
        with open(CONFIG_FILE, 'w') as f:
            json.dump(self.config, f)

    def update_music_volume(self):
        if self.config.get('mute', False):
            pygame.mixer.music.set_volume(0)
        else:
            master_vol = self.config['master'] / 10.0
            music_vol = self.config['music'] / 10.0
            final_vol = master_vol * music_vol
            pygame.mixer.music.set_volume(final_vol)
            
            if final_vol > 0 and not pygame.mixer.music.get_busy() and self.current_music:
                try:
                    pygame.mixer.music.load(os.path.join('assents', 'music', self.current_music))
                    pygame.mixer.music.play(-1)
                except: pass

    def load_audio(self):
        pygame.mixer.init()
        self.sounds = {}
        for snd in ['jump.wav', 'gameover.wav', 'platform_break.wav']:
            try:
                self.sounds[snd] = pygame.mixer.Sound(os.path.join('assents', 'sounds', snd))
            except:
                self.sounds[snd] = None
        try:
            pygame.mixer.music.load(os.path.join('assents', 'music', 'gameplay_music.mp3'))
        except:
            pass

    def play_sound(self, name):
        if self.config.get('mute', False):
            return
            
        master_vol = self.config['master'] / 10.0
        sfx_vol = self.config['sfx'] / 10.0
        final_vol = master_vol * sfx_vol
        
        if final_vol > 0 and self.sounds.get(name):
            self.sounds[name].set_volume(final_vol)
            self.sounds[name].play()

    def new(self):
        self.score = 0
        self.game_started = False
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)

        # Chão inicial
        self.ground = Platform(0, HEIGHT - 40, "static", WIDTH, 40)
        self.all_sprites.add(self.ground)
        self.platforms.add(self.ground)

        self.player.pos.y = self.ground.rect.top + 5
        self.player.vel.y = 0

        # Plataformas iniciais
        highest_y = self.ground.rect.top
        for i in range(8):
            new_y = highest_y - random.randint(70, 110)
            self.spawn_platform(new_y)
            highest_y = new_y
            
        self.run()

    def spawn_platform(self, y_pos):
        x_pos = random.randint(0, WIDTH - PLATFORM_WIDTH)
        p_type = random.choices(
            ["static", "moving", "breaking", "boost"], 
            weights=[65, 20, 10, 5]
        )[0]
        
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

        if not self.game_started:
            self.player.pos.y = self.ground.rect.top + 4
            self.player.vel.y = 0
            self.player.rect.midbottom = self.player.pos
            return

        if self.player.vel.y > 0:
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest_hit = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest_hit.rect.bottom:
                        lowest_hit = hit
                        
                if self.player.pos.y <= lowest_hit.rect.bottom:
                    self.player.pos.y = lowest_hit.rect.top + 5
                    self.player.vel.y = 0
                    self.player.state = 'squash'
                    
                    if lowest_hit.type == "boost":
                        self.player.vel.y = PLAYER_BOOST_JUMP
                    else:
                        self.player.jump()
                        
                    self.play_sound('jump.wav')
                    
                    if lowest_hit.type == "breaking":
                        lowest_hit.kill()
                        self.play_sound('platform_break.wav')

        # Câmera
        if self.player.rect.top <= HEIGHT / 2:
            self.player.pos.y += abs(self.player.vel.y)
            for plat in self.platforms:
                plat.rect.y += abs(self.player.vel.y)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10
                    
        while len(self.platforms) < 8:
            if len(self.platforms) > 0:
                highest_y = min([p.rect.y for p in self.platforms])
            else:
                highest_y = HEIGHT / 2

            new_y = highest_y - random.randint(70, 110)
            self.spawn_platform(new_y)

        # Game Over
        if self.player.rect.bottom > HEIGHT:
            self.playing = False
            self.play_sound('gameover.wav')
            pygame.mixer.music.stop()
            
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
                if event.key == pygame.K_SPACE and not self.game_started:
                    self.game_started = True
                    self.player.jump()
                    self.play_sound('jump.wav')

    def draw(self):
        if hasattr(self, 'bg') and self.bg:
            self.screen.blit(self.bg, (0, 0))
        else:
            self.screen.fill(DARK_GREY)
            
        self.all_sprites.draw(self.screen)
        
        if not self.game_started:
            lang = self.config['lang']
            c1 = self.font.render(TEXTS[lang]['controls_1'], True, WHITE)
            c2 = self.font.render(TEXTS[lang]['controls_2'], True, WHITE)
            c3 = self.font_large.render(TEXTS[lang]['controls_3'], True, YELLOW)
            
            self.screen.blit(c1, c1.get_rect(center=(WIDTH/2, HEIGHT/2 - 40)))
            self.screen.blit(c2, c2.get_rect(center=(WIDTH/2, HEIGHT/2)))
            self.screen.blit(c3, c3.get_rect(center=(WIDTH/2, HEIGHT/2 + 60)))
        else:
            score_text = self.font.render(f"Score: {self.score}", True, WHITE)
            self.screen.blit(score_text, (10, 10))
        
        pygame.display.flip()