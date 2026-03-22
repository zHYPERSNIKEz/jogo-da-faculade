import pygame
from game import Game
from menu import Menu

def main():
    pygame.init()
    game = Game()
    menu = Menu(game.screen, game)

    while True:
        action = menu.show_start_screen()
        
        if action == "exit":
            break
            
        game.play_music('gameplay_music.mp3')
        game.new()
        
        if not game.running:
            break
            
        if not menu.show_go_screen():
            break
            
        game.load_data()

    pygame.quit()

if __name__ == "__main__":
    main()