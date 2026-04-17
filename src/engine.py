from .utils.states import *
from .utils.enums import *

class Engine:
    def __init__(self):
        self.board = [0] * 25
        self.tigers = {0, 4, 20, 24}
        for i in self.tigers:
            self.board[i] = -1
        self.turn = Turn.GOAT
        self.phase = Phase.PLACEMENT
        self.goats_placed = 0
        self.goats_captured = 0
        self.winner = None

    def is_empty(self, pos):
        return self.board[pos] == 0

    def switch_turn(self):
        self.turn = Turn.TIGER if self.turn == Turn.GOAT else Turn.GOAT
    
    def get_piece(self):
        return self.turn.value

    def valid_normal_move(self, current, target):
        return target in N[current] and self.is_empty(target)

    def valid_jump_move(self, current, target):
        if (current, target) not in J:
            return False
        midpoint = J[(current, target)]
        return self.board[midpoint] == 1 and self.is_empty(target)
    
    def are_tigers_trapped(self):
        for t in self.tigers:
            for neighbor in N[t]:
                # if kunai position khali xa vane from tigers position, then tiger abhi zinda he lol
                if self.is_empty(neighbor):
                    return False
            # jump garna pai raxa vane tiger aajhai zinda xa
            for (start, end), mid in J.items():
                if start == t and self.board[mid] == 1 and self.is_empty(end):
                    return False
        # Tiger abhi zinda he lolllll
        return True