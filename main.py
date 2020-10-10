from game_loop import game_loop
from players import MinimaxPlayer, RandomPlayer
import pygame

pygame.init()

player1 = MinimaxPlayer(6)
player2 = MinimaxPlayer(6)

game_loop(player1, player2, freq=5)