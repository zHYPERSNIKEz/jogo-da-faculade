import pygame
from settings import *
import os

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.SysFont("arial", 48, bold=True)
        self.font_small = pygame.font.SysFont("arial", 20)
        
        try:
            pygame.mixer.music.load(os.path.join('assets', 'music', 'menu_music.mp3'))
            pygame.mixer.music.play(-1)
        except:
            pass

    def draw_text(self, text, font, color, y):
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect(center=(WIDTH/2, y))
        self.screen.blit(text_obj, text_rect)

    def show_start_screen(self):
        self.screen.fill(DARK_GREY)
        self.draw_text("ENDLESS JUMPER", self.font_title, WHITE, HEIGHT / 4)
        
        instructions = [
            "CONTROLES:",
            "A / D ou SETAS Esquerda/Direita para Mover",
            "Pulo é automático!",
            "",
            "Pressione ESPAÇO para Iniciar"
        ]
        
        y_offset = HEIGHT / 2
        for line in instructions:
            self.draw_text(line, self.font_small, WHITE, y_offset)
            y_offset += 30

        pygame.display.flip()
        return self.wait_for_key()

    def show_go_screen(self, score):
        self.screen.fill(RED)
        self.draw_text("GAME OVER", self.font_title, WHITE, HEIGHT / 4)
        self.draw_text(f"Pontuação: {score}", self.font_small, WHITE, HEIGHT / 2)
        self.draw_text("Pressione ESPAÇO para jogar novamente", self.font_small, WHITE, HEIGHT * 3/4)
        
        pygame.display.flip()
        return self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
                    if event.key == pygame.K_SPACE:
                        return True
        return False