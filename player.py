import pygame
import os
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Tenta carregar o sprite, senão usa um quadrado azul
        try:
            self.image = pygame.image.load(os.path.join('assets', 'sprites', 'player.png')).convert_alpha()
        except:
            self.image = pygame.Surface((40, 40))
            self.image.fill(BLUE)
            
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        
        self.vel = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2(self.rect.center)

    def update(self):
        # Aplicar gravidade
        self.vel.y += GRAVITY
        
        # Movimentação Horizontal
        keys = pygame.key.get_pressed()
        self.vel.x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel.x = -PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel.x = PLAYER_SPEED

        # Atualiza a posição
        self.pos += self.vel
        
        # Faz o personagem dar a volta na tela
        if self.pos.x > WIDTH + 20:
            self.pos.x = -20
        if self.pos.x < -20:
            self.pos.x = WIDTH + 20
            
        self.rect.midbottom = self.pos

    def jump(self):
        self.vel.y = PLAYER_JUMP