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
PLAYER_BOOST_JUMP = -22

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (40, 200, 40)
BLUE = (50, 150, 255)
RED = (200, 40, 40)
YELLOW = (255, 255, 0)
DARK_GREY = (40, 40, 40)

# Configurações de Plataforma
PLATFORM_WIDTH = 80
PLATFORM_HEIGHT = 15

# Arquivos de Save
HS_FILE = "highscore.txt"
CONFIG_FILE = "config.json"

# Traduções
TEXTS = {
    'pt': {
        'title': 'ENDLESS JUMPER',
        'play': 'JOGAR',
        'settings': 'CONFIGURACOES',
        'exit': 'SAIR',
        'record': 'RECORDE ATUAL:',
        'language': 'IDIOMA: PT-BR',
        'master': 'SOM GERAL:',
        'music': 'MUSICA:',
        'sfx': 'EFEITOS:',
        'on': 'LIGADO',
        'off': 'DESLIGADO',
        'back': 'VOLTAR',
        'controls_1': 'A / D ou SETAS para Mover',
        'controls_2': 'O pulo eh automatico!',
        'controls_3': 'APERTE ESPACO PARA INICIAR',
        'game_over': 'FIM DE JOGO',
        'score': 'Sua Pontuacao:',
        'new_record': 'NOVO RECORDE!',
        'play_again': 'Pressione ESPACO para voltar ao menu'
    },
    'en': {
        'title': 'ENDLESS JUMPER',
        'play': 'PLAY',
        'settings': 'SETTINGS',
        'exit': 'EXIT',
        'record': 'CURRENT BEST:',
        'language': 'LANGUAGE: EN',
        'master': 'MASTER SOUND:',
        'music': 'MUSIC:',
        'sfx': 'SFX:',
        'on': 'ON',
        'off': 'OFF',
        'back': 'BACK',
        'controls_1': 'A / D or ARROWS to Move',
        'controls_2': 'Jumping is automatic!',
        'controls_3': 'PRESS SPACE TO START',
        'game_over': 'GAME OVER',
        'score': 'Your Score:',
        'new_record': 'NEW RECORD!',
        'play_again': 'Press SPACE to return to menu'
    }
}