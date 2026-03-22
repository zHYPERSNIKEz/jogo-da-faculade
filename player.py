import pygame
import os
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = {}
        states = ['standard', 'squash', 'stretch', 'front']
        
        sizes = {
            'standard': (40, 40),
            'squash': (50, 30),
            'stretch': (30, 50),
            'front': (40, 40)
        }
        
        for state in states:
            try:
                img = pygame.image.load(os.path.join('assents', 'sprites', f'player_{state}.png')).convert_alpha()
                self.images[state] = pygame.transform.scale(img, sizes[state])
            except:
                surf = pygame.Surface(sizes[state])
                surf.fill(RED)
                self.images[state] = surf

        self.state = 'standard'
        self.image = self.images[self.state]
        self.rect = self.image.get_rect()
        
        self.vel = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2(WIDTH / 2, HEIGHT / 2)
        self.squash_timer = 0 

    def update(self):
        self.vel.y += GRAVITY
        
        keys = pygame.key.get_pressed()
        self.vel.x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel.x = -PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel.x = PLAYER_SPEED

        self.pos += self.vel
        
        if self.pos.x > WIDTH + 20:
            self.pos.x = -20
        if self.pos.x < -20:
            self.pos.x = WIDTH + 20
            
        if self.squash_timer > 0:
            self.state = 'squash'
            self.squash_timer -= 1
        else:
            if self.vel.y < -2:
                self.state = 'stretch'
            elif self.vel.y > 2:
                self.state = 'front'
            else:
                self.state = 'standard'
                
        self.image = self.images[self.state]
        
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.pos

    def jump(self):
        self.vel.y = PLAYER_JUMP
        self.squash_timer = 5