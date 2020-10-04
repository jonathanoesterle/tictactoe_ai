# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 19:08:25 2020

@author: joesterle
"""

import pygame
import numpy as np

import time
import neat

from tictactoe import TicTacToe_2players
from utils import game_exit
from players import RandomPlayer, AIPlayer

pygame.font.init()  # init font
      


def game_loop(player1=None, player2=None):
    
    clock = pygame.time.Clock()
    pygame.display.set_caption("TicTacToe")
    
    player1 = player1 or RandomPlayer()
    player2 = player2 or RandomPlayer()

    winw = 400
    winh = 400
    win = pygame.display.set_mode((winw, winh))
    

    game = TicTacToe_2players(win, player1, player2)
    
    while True: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit()

            # elif event.type == pygame.MOUSEBUTTONDOWN:
            #     if pygame.mouse.get_pressed()[0]: # check for left click.
            #         pos = pygame.mouse.get_pos() # check click pos                 
            #         print(f'clicked at {pos}')
            #         game.clicked(pos)
        
        game.action()  
        
        win.fill((255,255,255))                
        game.draw(f'1:{game.ttt.n1won}, 2:{game.ttt.n1won}, T:{game.ttt.nties}')
        pygame.display.update()
        clock.tick(2)
        
        if game.ttt.finished:               
            game.ttt.reset()
            time.sleep(2)

def eval_genomes(genomes, config):
    
    global opponent_player
    
    winw = 800
    winh = 800
    
    plt_max = 0
    plt_max_x = 0
    assert plt_max_x**2 == plt_max
    
    if plt_max > 0:
        clock = pygame.time.Clock()
        win = pygame.display.set_mode((winw, winh))
        pygame.display.set_caption("TicTacToe")
    else:
        win = None
    
    n_genomes = len(genomes)
    
    ge = []
    games = []
    
    nxplot = np.min([plt_max_x, int(np.ceil(np.sqrt(n_genomes)))])
    
    for idx, (genome_id, genome) in enumerate(genomes):
        genome.fitness = 0
        ge.append(genome)
        
        if idx < plt_max:
            col = idx % nxplot
            row = int(np.floor(idx/nxplot))
    
            dwinw = float(1 / nxplot)
            dwinh = float(1 / nxplot)
            
            rect=(col*dwinw, row*dwinh, 1/nxplot, 1/nxplot)
        else:
            rect = None
            
        player1 = AIPlayer(neat.nn.FeedForwardNetwork.create(genome, config))
        
        games.append(TicTacToe_2players(win, player1=player1, player2=opponent_player, rect=rect))
    
    ge = np.array(ge)
    games = np.array(games)

    run = True
    
    playing_idx = np.ones(len(games), dtype=bool)
    max_rounds = 40
    played_rounds = np.zeros(len(games), dtype=int)
    paused_turns = np.zeros(len(games), dtype=int)

    def draw():
        if plt_max > 0: win.fill((255,255,255))
        for g, game in zip(ge[:plt_max], games[:plt_max]):
            game.draw(info=f'{g.fitness:.1f}')
        
        if plt_max > 0: pygame.display.update()

    while run and np.any(playing_idx):
        
        if plt_max > 0:
            clock.tick(120)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit()

        for g, game in zip(ge[playing_idx], games[playing_idx]):
            if not game.ttt.finished:
                ntrials = game.action()
                g.fitness -= 0.05 * ntrials


        for idx, (g, game) in enumerate(zip(ge, games)):
            if game.ttt.finished and playing_idx[idx]:
                played_rounds[idx] += 1
                
                if paused_turns[idx] == 0:
                    if game.ttt.player_won == 1:
                        g.fitness += 2
                    if game.ttt.player_won == -1:
                        g.fitness -= 1
                    else:
                        g.fitness += 0.2
                        
                if played_rounds[idx] > max_rounds:
                    playing_idx[idx] = False
                else:
                    paused_turns[idx] += 1

                if paused_turns[idx] > 3:
                    paused_turns[idx] = 0
                    game.ttt.reset()

        draw()
    draw()


config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                      neat.DefaultSpeciesSet, neat.DefaultStagnation,
                      'config-feedforward.txt')



def train_AI(ngens=10):
    
    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)
    
    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    #p.add_reporter(neat.Checkpointer(5))
    
    return p.run(eval_genomes, ngens)

print('go!')

opponent_player = RandomPlayer()

for i in range(3):
    winner = train_AI(ngens=4+i*2)
    opponent_player = AIPlayer(neat.nn.FeedForwardNetwork.create(winner, config))

player1 = AIPlayer(neat.nn.FeedForwardNetwork.create(winner, config))
game_loop(player1, RandomPlayer())