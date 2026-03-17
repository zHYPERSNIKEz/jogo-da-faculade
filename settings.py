import pygame

# Configurações da Tela
WIDTH = 480
HEIGHT = 600
FPS = 60
TITLE = "Endless Jumper"

# Física do Jogador
GRAVITY = 0.6
PLAYER_SPEED = 7
PLAYER_JUMP = -14

# Cores (usadas caso os sprites não existam)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (40, 200, 40)
BLUE = (50, 150, 255)
RED = (200, 40, 40)
DARK_GREY = (40, 40, 40)

# Configurações de Plataforma
PLATFORM_WIDTH = 80
PLATFORM_HEIGHT = 15

# Arquivo de High Score
HS_FILE = "highscore.txt"