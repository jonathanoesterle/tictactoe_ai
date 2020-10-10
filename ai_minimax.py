import random

import numpy as np

from tictactoe import TicTacToe
from copy import deepcopy
import itertools

class TicTacToe_minimax_state():

	def __init__(self, tictactoe):
		self.ttt = deepcopy(tictactoe)

	def get_child_states(self):
		child_states = []
		for row, col in itertools.product(range(3), range(3)):
			if self.ttt.state[row, col] == 0:
				child_state = TicTacToe_minimax_state(self.ttt)
				child_state.ttt.clicked(row, col)
				child_states.append((child_state, (row, col)))
		random.shuffle(child_states)
		return child_states

	def get_value(self):
		if self.ttt.finished:
			return self.ttt.player_won
		else:
			return 0.0

	def is_finished(self):
		return self.ttt.finished


def minimax(state, depth, isMaxPlayer, alpha=np.NINF, beta=np.inf):
	best_pos = None

	if depth == 0 or state.is_finished():
		return state.get_value(), best_pos

	if isMaxPlayer:
		maxEval = np.NINF
		for child_state, pos in state.get_child_states():
			eval, _ = minimax(state=child_state, depth=depth-1, isMaxPlayer=False, alpha=alpha, beta=beta)
			if eval > maxEval:
				maxEval = eval
				best_pos = pos
			alpha = max(alpha, eval)
			if beta <= alpha:
				break
		return maxEval, best_pos
	else:

		minEval = np.inf
		for child_state, pos in state.get_child_states():
			eval, _ = minimax(state=child_state, depth=depth-1, isMaxPlayer=True, alpha=alpha, beta=beta)
			if eval < minEval:
				minEval = eval
				best_pos = pos
			beta = min(beta, eval)
			if beta <= alpha:
				break
		return minEval, best_pos