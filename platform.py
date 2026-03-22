import pygame
import random
import os
from settings import *

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, p_type="static", width=PLATFORM_WIDTH, height=PLATFORM_HEIGHT, score=0):
        super().__init__()
        self.type = p_type
        
        colors = {"static": GREEN, "moving": BLUE, "breaking": RED, "boost": YELLOW}
        
        try:
            if self.type == "static" or self.type == "moving":
                img_name = 'platform.png'
            else:
                img_name = f'platform_{self.type}.png'
                
            loaded_img = pygame.image.load(os.path.join('assents', 'sprites', img_name)).convert_alpha()
            self.image = pygame.transform.scale(loaded_img, (width, height))
        except:
            self.image = pygame.Surface((width, height))
            self.image.fill(colors.get(self.type, GREEN))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        if self.type == "moving" or (self.type == "breaking" and score >= 200):
            self.speed = random.choice([-3, -2, 2, 3])
        else:
            self.speed = 0

    def update(self):
        if self.speed != 0:
            self.rect.x += self.speed
            if self.rect.right > WIDTH or self.rect.left < 0:
                self.speed *= -1