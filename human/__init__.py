from builtins import range, input
import numpy as np


class Human:
    def __init__(self):
        pass

    def set_symbol(self, sym):
        self.sym = sym

    def take_action(self, env):
        while True:
            # Break se fizermos um movimento legal
            move = input(
                "Insira as coordenadas i, j para o próximo movimento (por exemplo: 0,2): ")
            i, j = move.split(',')
            i = int(i)
            j = int(j)
            if env.is_empty(i, j):
                env.board[i, j] = self.sym
                break

    def update(self, env):
        pass

    def update_state_history(self, s):
        pass
