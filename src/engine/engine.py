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
        return self.board[midpoint] == 1 and self.is_empty(target) and self.board[current] == -1
    
    def place_goat(self, pos):
        if self.turn != Turn.GOAT or self.phase != Phase.PLACEMENT or not self.is_empty(pos) or self.winner is not None:
            return False
        self.board[pos] = 1
        self.goats_placed += 1
        if self.goats_placed == 20:
            self.phase = Phase.MOVEMENT
        self.switch_turn()
        self.check_winner()
        return True

    def move_goat(self,current,target):
        if not self.valid_normal_move(current, target) or self.phase != Phase.MOVEMENT or self.winner is not None:
            return False
        self.board[current] = 0
        self.board[target] = 1
        self.switch_turn()
        self.check_winner()
        return True

    def tiger_normal_move(self,current,target):
        self.board[current] = 0
        self.board[target] = -1
        self.tigers.remove(current)
        self.tigers.add(target)
        return True

    def tiger_jump_move(self,current,target):
        mid = J[(current, target)]
        self.board[current] = 0
        self.board[target] = -1
        self.board[mid] = 0
        self.tigers.remove(current)
        self.tigers.add(target)
        self.goats_captured += 1
        return True

    def move_tiger(self,current,target):
        if self.turn != Turn.TIGER or self.phase != Phase.MOVEMENT or self.winner is not None:
            return False
        moved = False
        if self.valid_normal_move(current,target):
            moved = self.tiger_normal_move(current,target)
        elif self.valid_jump_move(current, target):
            moved = self.tiger_jump_move(current, target)
        if moved:
            self.switch_turn()
            self.check_winner()
        return moved

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
    
    def check_winner(self):
        if self.goats_captured >= 5:
            self.winner = Turn.TIGER
        elif self.are_tigers_trapped():
            self.winner = Turn.GOAT