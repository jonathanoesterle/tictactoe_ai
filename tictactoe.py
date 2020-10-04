# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 14:16:20 2020

@author: joesterle
"""

import numpy as np
from utils import draw_text, tocolor
import pygame

class TicTacToe():
    
    def __init__(self):
        
        self.player_turn = 1#np.random.choice([1,-1])
        self.state = np.zeros((3,3),dtype=int)
        self.finished = False
        self.player_won = 0
        self.nties = 0
        self.n1won = 0
        self.n2won = 0
                
    
    def clicked(self, row, col):
        if self.finished:
            self.reset()
        else:
            if self.state[row,col] == 0:
                self.state[row,col] = self.player_turn
                self.player_turn = -1 if self.player_turn == 1 else 1
            
                self.check_win()
                if not self.finished:
                    self.check_full()


    def check_win(self):
        
        def row_complete(row):
            assert row.size == 3, row
            if np.all(row != 0) and (np.unique(row).size == 1):
                return True
            else:
                return False
        
        for idx in range(3):
            if row_complete(self.state[idx,:]):
                self.finished = True
                self.player_won = self.state[idx,0]

            if row_complete(self.state[:,idx]):
                self.finished = True
                self.player_won = self.state[0,idx]
              
            
        if row_complete(np.diag(np.rot90(self.state))) or row_complete(np.diag(self.state)):
            self.finished = True
            self.player_won = self.state[1,1]
        
        if self.finished:
            if self.player_won == 1:
                self.n1won += 1
            elif self.player_won == -1:
                self.n2won += 1
            else:
                raise ValueError(self.player_won)
        
        
    def check_full(self):
        if np.all(self.state != 0):
            self.finished = True
            self.nties += 1
            
    def reset(self):
        self.state[:] = 0
        self.finished = False
        self.player_won = 0
        self.player_turn = np.random.choice([1,-1])

class TicTacToe_surface():
    
    def __init__(self, win, tictactoe, rect=(0,0,1,1)):
        self.ttt = tictactoe
        
        if (rect is None) or (win is None):
            self.win = None
        else:
            self.win = win
            
            self.winw, self.winh = win.get_size()
            
            x0 = rect[0]*self.winw
            y0 = rect[1]*self.winh
            
            self.x0 = x0
            self.y0 = y0
            
            x1 = x0 + rect[2]*self.winw
            y1 = y0 + rect[3]*self.winh
            
            self.x1 = x1
            self.y1 = y1
            
            xrng = x1-x0
            yrng = y1-y0
            
            self.xrng = xrng
            self.yrng = yrng
            
            self.vl1 = ((1 * xrng / 3. + x0, y0), (1 * xrng / 3. + x0, y1))
            self.vl2 = ((2 * xrng / 3. + x0, y0), (2 * xrng / 3. + x0, y1))
            
            self.vl3 = ((x0, y0), (x0, y1))
            self.vl4 = ((x1, y0), (x1, y1))
            
            self.hl1 = ((x0, 1 * yrng / 3. + y0), (x1, 1 * yrng / 3. + y0))
            self.hl2 = ((x0, 2 * yrng / 3. + y0), (x1, 2 * yrng / 3. + y0))
    
            self.hl3 = ((x0, y0), (x1, y0))
            self.hl4 = ((x0, y1), (x1, y1))
            
            self.lc = (0,0,0)
            
    
            xdist = np.linspace(x0+xrng/6, x0+xrng*5/6, 3)
            ydist = np.linspace(y0+yrng/6, y0+yrng*5/6, 3)        
            self.centx, self.centy = np.meshgrid(xdist, ydist)

    def draw(self, info=None):
        
        if self.win is None: return
        
            
        ntotal = self.ttt.n1won+ self.ttt.n2won + self.ttt.nties
        
        if ntotal > 0:
            yfrac1 = self.ttt.n1won / ntotal
            yfrac2 = self.ttt.n2won / ntotal
            
            self.win.fill(tocolor('gray'), (self.x0, self.y0, self.xrng, self.yrng))
            self.win.fill(tocolor('indianred'), (self.x0, self.y1-yfrac1*self.yrng, self.xrng, yfrac1*self.yrng))
            self.win.fill(tocolor('cyan'), (self.x0, self.y0, self.xrng, yfrac2*self.yrng))
            
        
        for (l_start, l_end) in [self.vl1, self.vl2, self.hl1, self.hl2]:
            pygame.draw.line(self.win, self.lc, l_start, l_end, 2)
            
        for (l_start, l_end) in [self.hl3, self.hl4, self.vl3, self.vl4]:
            pygame.draw.line(self.win, self.lc, l_start, l_end, 6)
        
        
        for i in range(3):
            for j in range(3):
                if self.ttt.state[i,j] != 0:
                    mark = 'X' if self.ttt.state[i,j] == 1 else 'O'
                    color = 'darkred' if self.ttt.state[i,j] == 1 else 'blue'
                    draw_text(self.win, mark, xy=(self.centx[i,j],self.centy[i,j]), color=color)
                    
        if info is not None:
            draw_text(self.win, info, xy=(self.centx[1,1], self.centy[1,1]-self.yrng/9), color='black')

            
    def clicked(self, pos):
        posx, posy= pos
            
        if posx < self.vl1[0][0]:
            col = 0
        elif posx > self.vl2[0][0]:
            col = 2
        else:
            col = 1
            
        if posy < self.hl1[0][1]:
            row = 0
        elif posy > self.hl2[0][1]:
            row = 2
        else:
            row = 1
            
        self.ttt.clicked(row, col)
        
        
class TicTacToe_2players():
    def __init__(self, win, player1, player2, rect=(0,0,1,1)):
        
        self.ttt = TicTacToe()
        self.surface = TicTacToe_surface(win, self.ttt, rect=rect)
        self.player1 = player1
        self.player2 = player2

        
    def action(self):
        ntrials = 0
        
        if not self.ttt.finished:
            if self.ttt.player_turn == 1:
                active_player = self.player1
            elif self.ttt.player_turn == -1:
                active_player = self.player2
            else:
                raise ValueError()
                
            if active_player.auto:
                ntrials = active_player.action(self.ttt)
            else:
                ntrials = active_player.action(self.surface)
                
        return ntrials
                
    def draw(self, info=None):
        self.surface.draw(info=info)
        

    def clicked(self, pos):
        self.surface.clicked(pos)