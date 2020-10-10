import time
import pygame
from tictactoe import TicTacToe_2players
from utils import game_exit


def game_loop(player1, player2, freq=10):
    clock = pygame.time.Clock()

    winw, winh = 400, 400
    win = pygame.display.set_mode((winw, winh))
    pygame.display.set_caption("TicTacToe")

    game = TicTacToe_2players(win, player1, player2)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit()

        win.fill((255, 255, 255))
        game.draw(f'1:{game.ttt.n1won}, 2:{game.ttt.n2won}, T:{game.ttt.nties}')
        pygame.display.update()
        clock.tick(freq)

        if game.ttt.finished:
            time.sleep(10/freq)
            game.ttt.reset()

        else:
            game.action()