from .utils.states import *
from .utils.enums import *

class Engine:
    def __init__(self):
        self.board = [0] * 25
        for i in [0, 4, 20, 24]:
            self.board[i] = -1
        self.turn = Turn.GOAT
        self.phase = Phase.PLACEMENT
        self.goats_placed = 0
        self.goats_captured = 0
        self.winner = None

    def is_empty(self, pos):
        return self.board[pos] == 0

    def valid_normal_move(self, current, target):
        return target in N[current] and self.is_empty(target)

    def valid_jump_move(self, current, target):
        if (current, target) not in J:
            return False
        midpoint = J[(current, target)]
        return self.board[midpoint] == 1 and self.is_empty(target)