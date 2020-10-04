# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 14:14:38 2020

@author: joesterle
"""

from matplotlib import colors
import pygame
import sys

def tocolor(color):
    if isinstance(color, str):
        return tuple([int(255*ci) for ci in colors.to_rgb(color)])
    elif isinstance(color, tuple):
        if isinstance(color[0], float):
            return tuple([int(255*ci) for ci in color])
        elif isinstance(color[0], int):
            return color
        else:
            raise
    else:
        raise
        

# Exit game.
def game_exit():
    pygame.quit()
    sys.exit()

# Create text object.
def text_objects(text, font, c='black'):
    textSurface = font.render(text, True, tocolor(c))
    return textSurface, textSurface.get_rect()

# Show text.
def draw_text(win, text, xy, font='freesansbold.ttf', size=20, color='black'):
    
    font = pygame.font.Font('freesansbold.ttf',size)
    TextSurf, TextRect = text_objects(str(text), font, tocolor(color))
    TextRect.center = xy
    win.blit(TextSurf, TextRect)