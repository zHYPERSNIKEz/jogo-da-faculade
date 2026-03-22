import pygame
from settings import *
import os

class Menu:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.font_title = pygame.font.SysFont("arial", 48, bold=True)
        self.font_medium = pygame.font.SysFont("arial", 28, bold=True)
        self.font_small = pygame.font.SysFont("arial", 20)

    def get_text(self, key):
        return TEXTS[self.game.config['lang']][key]

    def draw_text(self, text, font, color, y, x=WIDTH/2):
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect(center=(x, y))
        self.screen.blit(text_obj, text_rect)

    def show_start_screen(self):
        options = ["play", "settings", "exit"]
        selected = 0
        waiting = True

        self.game.play_music('menu_music.mp3')

        while waiting:
            self.screen.fill(DARK_GREY)
            self.draw_text(self.get_text('title'), self.font_title, WHITE, HEIGHT / 4)
            self.draw_text(f"{self.get_text('record')} {self.game.highscore}", self.font_small, GREEN, HEIGHT / 3)

            for i, opt in enumerate(options):
                color = YELLOW if i == selected else WHITE
                self.draw_text(self.get_text(opt), self.font_medium, color, HEIGHT / 2 + i * 50)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected = (selected - 1) % len(options)
                        self.game.play_sound('jump.wav')
                    if event.key == pygame.K_DOWN:
                        selected = (selected + 1) % len(options)
                        self.game.play_sound('jump.wav')
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        self.game.play_sound('platform_break.wav')
                        if options[selected] == "play":
                            return "play"
                        elif options[selected] == "settings":
                            self.show_settings_screen()
                        elif options[selected] == "exit":
                            return "exit"

    def show_settings_screen(self):
        options = ["language", "mute", "master", "music", "sfx", "back"]
        selected = 0
        waiting = True

        while waiting:
            self.screen.fill(DARK_GREY)
            self.draw_text(self.get_text('settings'), self.font_title, WHITE, HEIGHT / 5)

            for i, opt in enumerate(options):
                color = YELLOW if i == selected else WHITE
                text_to_draw = ""
                
                if opt == "language":
                    text_to_draw = self.get_text('language')
                elif opt == "mute":
                    checkbox = "[ X ]" if self.game.config.get('mute', False) else "[   ]"
                    texto_base = "MUDAR TUDO:" if self.game.config['lang'] == 'pt' else "MUTE ALL:"
                    text_to_draw = f"{texto_base} {checkbox}"
                elif opt in ["master", "music", "sfx"]:
                    val = self.game.config[opt]
                    status = str(val) if val > 0 else self.get_text('off')
                    text_to_draw = f"{self.get_text(opt)} < {status} >"
                elif opt == "back":
                    text_to_draw = self.get_text('back')

                self.draw_text(text_to_draw, self.font_medium, color, HEIGHT / 2.5 + i * 45)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected = (selected - 1) % len(options)
                        self.game.play_sound('jump.wav')
                    if event.key == pygame.K_DOWN:
                        selected = (selected + 1) % len(options)
                        self.game.play_sound('jump.wav')
                        
                    opt = options[selected]
                    
                    if opt in ["master", "music", "sfx"]:
                        if event.key == pygame.K_LEFT:
                            self.game.config[opt] = max(0, self.game.config[opt] - 1)
                            self.game.update_music_volume()
                            self.game.play_sound('jump.wav')
                            self.game.save_config()
                        elif event.key == pygame.K_RIGHT:
                            self.game.config[opt] = min(10, self.game.config[opt] + 1)
                            self.game.update_music_volume()
                            self.game.play_sound('jump.wav')
                            self.game.save_config()

                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        self.game.play_sound('platform_break.wav')
                        
                        if opt == "language":
                            self.game.config['lang'] = 'en' if self.game.config['lang'] == 'pt' else 'pt'
                            self.game.save_config() 
                        elif opt == "mute":
                            self.game.config['mute'] = not self.game.config.get('mute', False)
                            self.game.update_music_volume()
                            self.game.save_config()
                        elif opt == "back":
                            waiting = False

    def show_go_screen(self):
        self.screen.fill(RED)
        self.draw_text(self.get_text('game_over'), self.font_title, WHITE, HEIGHT / 4)
        
        self.draw_text(f"{self.get_text('score')} {self.game.score}", self.font_small, WHITE, HEIGHT / 2 - 20)
        
        if self.game.score > self.game.highscore:
            self.draw_text(self.get_text('new_record'), self.font_small, GREEN, HEIGHT / 2 + 20)
        else:
            self.draw_text(f"{self.get_text('record')} {self.game.highscore}", self.font_small, WHITE, HEIGHT / 2 + 20)
            
        self.draw_text(self.get_text('play_again'), self.font_small, WHITE, HEIGHT * 3/4)
        
        pygame.display.flip()
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                        return True
        return False