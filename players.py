# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 14:19:09 2020

@author: joesterle
"""

import numpy as np
import pygame
from utils import game_exit

class Player():
    def __init__(self):
        self.auto = True

class HumanPlayer(Player):
    
    def __init__(self):
        self.auto = False
    
    @staticmethod
    def action(surface):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit()
    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]: # check for left click.
                        pos = pygame.mouse.get_pos() # check click pos                 
                        print(f'clicked at {pos}')
                        surface.clicked(pos)
                        return 0

class RandomPlayer(Player):
    
    def __init__(self):
        self.auto = True
    
    @staticmethod
    def action(tictactoe):
        
        assert np.any(tictactoe.state == 0)

        def get_random_indexes():
            row, col = np.random.randint(0,3,(2))
            return row, col
        
        row, col = get_random_indexes()
        while tictactoe.state[row, col] != 0:
            row, col = get_random_indexes()
        tictactoe.clicked(row, col)
        
        return 0
        
class AIPlayer():
    
    def __init__(self, net):
        self.auto = True
        self.net = net
    
    def action(self, tictactoe):
        
        assert np.any(tictactoe.state == 0)
        
        output = self.net.activate(tictactoe.state.flatten())
        
        sortidx = np.flip(np.argsort(output))
        
        for ntrials, idx in enumerate(sortidx):
            
            row = idx % 3
            col = int(idx / 3)
            
            if tictactoe.state[row, col] == 0:
                tictactoe.clicked(row, col)
                
                return ntrials