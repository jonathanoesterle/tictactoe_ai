# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 19:08:25 2020

@author: joesterle
"""

import pygame
import numpy as np

import time
import neat

from game_loop import game_loop
from tictactoe import TicTacToe_2players
from utils import game_exit
from players import RandomPlayer, AIPlayer, HumanPlayer, DetPlayer

pygame.font.init()  # init font


def eval_genomes(genomes, config):
    global rounds_per_genom, opponent_player, n_gen

    winw = 800
    winh = 800

    if n_gen % 10 == 0:
        plt_max = plt_max_x ** 2
    else:
        plt_max = 0

    if plt_max > 0:
        clock = pygame.time.Clock()
        win = pygame.display.set_mode((winw, winh))
        pygame.display.set_caption("TicTacToe")
    else:
        win = None

    n_genomes = len(genomes)

    ge = []
    games = []

    for idx, (genome_id, genome) in enumerate(genomes):
        genome.fitness = 0.5 * rounds_per_genom
        ge.append(genome)

        if idx < plt_max:
            col = idx % plt_max_x
            row = int(np.floor(idx / plt_max_x))

            dwinw = float(1 / plt_max_x)
            dwinh = float(1 / plt_max_x)

            rect = (col * dwinw, row * dwinh, 1 / plt_max_x, 1 / plt_max_x)
        else:
            rect = None

        player1 = AIPlayer(neat.nn.FeedForwardNetwork.create(genome, config))

        games.append(TicTacToe_2players(win, player1=player1, player2=opponent_player, rect=rect))

    ge = np.array(ge)
    games = np.array(games)

    run = True

    playing_idx = np.ones(len(games), dtype=bool)
    played_rounds = np.zeros(len(games), dtype=int)
    paused_turns = np.zeros(len(games), dtype=int)

    def draw():
        if plt_max > 0: win.fill((255, 255, 255))
        for g, game in zip(ge[:plt_max], games[:plt_max]):
            game.draw(info=f'{g.fitness:.1f}')

        if plt_max > 0: pygame.display.update()

    while run and np.any(playing_idx):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit()

        if plt_max > 0: clock.tick(120)

        for g, game in zip(ge[playing_idx], games[playing_idx]):
            if not game.ttt.finished:
                ntrials = game.action()
                g.fitness -= 0.1 * ntrials

        for idx, (g, game) in enumerate(zip(ge, games)):
            if game.ttt.finished and playing_idx[idx]:
                played_rounds[idx] += 1

                if paused_turns[idx] == 0:
                    if game.ttt.player_won == 1:
                        g.fitness += 2
                    if game.ttt.player_won == -1:
                        g.fitness -= 2
                    else:
                        g.fitness += 1

                if played_rounds[idx] > rounds_per_genom:
                    playing_idx[idx] = False

                paused_turns[idx] += 1

                if paused_turns[idx] > 3:
                    paused_turns[idx] = 0
                    game.ttt.reset()

        draw()
    draw()
    n_gen += 1


config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                            neat.DefaultSpeciesSet, neat.DefaultStagnation,
                            'config-feedforward.txt')


def train_ai(ngens=10):
    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    # p.add_reporter(neat.Checkpointer(5))

    return p.run(eval_genomes, ngens)


print('go!')

import pickle

global plt_max_x, rounds_per_genom, n_gen

load = False
plt_max_x = 6
rounds_per_genom = 30

if not load:

    opponent_player = RandomPlayer()
    for i in range(2):
        n_gen = 0
        winner = train_ai(ngens=100)
        opponent_player = AIPlayer(neat.nn.FeedForwardNetwork.create(winner, config))

    pickle.dump(winner, open(f"winner{i}.p", "wb"))

else:
    winner = pickle.load(open(f"winner0.p", "rb"))

player1 = AIPlayer(neat.nn.FeedForwardNetwork.create(winner, config))
game_loop(player1, RandomPlayer())
# game_loop(player1, player1)
