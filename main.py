import pygame
from game import Game
from menu import Menu

def main():
    pygame.init()
    game = Game()
    menu = Menu(game.screen)

    # Passa o recorde salvo para a tela inicial
    if not menu.show_start_screen(game.highscore):
        pygame.quit()
        return

    while game.running:
        game.new()
        
        if game.running:
            # Passa a pontuação da partida E o recorde antigo para a tela de Game Over
            if not menu.show_go_screen(game.score, game.highscore):
                game.running = False
            # Atualiza a variável de recorde caso o jogador tenha batido na partida anterior
            game.load_data()

    pygame.quit()

if __name__ == "__main__":
    main()