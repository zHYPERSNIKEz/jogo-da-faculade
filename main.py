import pygame
from game import Game
from menu import Menu

def main():
    pygame.init()
    game = Game()
    menu = Menu(game.screen)

    # Tela Inicial
    if not menu.show_start_screen():
        pygame.quit()
        return

    # Loop Principal da Aplicação
    while game.running:
        game.new()
        
        # Após perder, se o jogo ainda estiver rodando (não foi fechado),
        # exibe a tela de Game Over. Se o usuário quiser sair, para o loop.
        if game.running:
            if not menu.show_go_screen(game.score):
                game.running = False

    pygame.quit()

if __name__ == "__main__":
    main()