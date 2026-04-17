from .utils.states import *
from .utils.enums import *
from dataclasses import dataclass

@dataclass
class History:
    sid: str
    move: str
    piece: str
    current: int = None
    target: int = None
    phase: Phase = None
    captured: int = None
    # paxi datetime pani halda hunxa

class Engine:
    def __init__(self):
        self.board = [0] * 25
        self.tigers = {0, 4, 20, 24}
        for i in self.tigers:
            self.board[i] = -1
        self.turn = Player.GOAT
        self.phase = Phase.PLACEMENT
        self.goats_placed = 0
        self.goats_captured = 0
        self.winner = None
        self.history = []

    def is_empty(self, pos):
        return self.board[pos] == 0

    def _end_turn(self):
        self.turn = Player.TIGER if self.turn == Player.GOAT else Player.GOAT
        self.check_winner()
    
    # def get_piece(self):
    #     return self.turn.value

    def valid_normal_move(self, current, target):
        return target in N[current] and self.is_empty(target)

    def valid_jump_move(self, current, target):
        if (current, target) not in J:
            return False
        midpoint = J[(current, target)]
        return self.board[midpoint] == Player.GOAT.value and self.is_empty(target)
    
    def place_goat(self, pos, sid=None, role=None,):
        if (self.turn != Player.GOAT or self.phase != Phase.PLACEMENT or not self.is_empty(pos) or self.winner or (role is not None and role != Player.GOAT.value)):
            return False
        self.board[pos] = Player.GOAT.value
        self.goats_placed += 1
        if self.goats_placed == 20:
            self.phase = Phase.MOVEMENT
        self.history.append(History(sid=sid, move="place", piece=Player.GOAT.name, current=None, target=pos, phase=self.phase.value))
        self._end_turn()
        return True

    def move_goat(self,current,target,sid=None,role=None):
        if (self.turn != Player.GOAT or self.phase != Phase.MOVEMENT or self.winner or not self.valid_normal_move(current, target) or (role is not None and role != Player.GOAT.value)):
            return False
        self.board[current] = 0
        self.board[target] = Player.GOAT.value
        self.history.append(History(sid=sid, move="move", piece=Player.GOAT.name, current=current, target=target, phase=self.phase.value))
        self._end_turn()
        self.check_winner()
        return True

    def tiger_normal_move(self,current,target,sid=None):
        self.board[current] = 0
        self.board[target] = -1
        self.tigers.remove(current)
        self.tigers.add(target)
        self.history.append(History(sid=sid, move="move", piece=Player.TIGER.name, current=current, target=target, phase=self.phase.value))
        return True

    def tiger_jump_move(self,current,target,sid=None):
        mid = J[(current, target)]
        self.board[current] = 0
        self.board[target] = -1
        self.board[mid] = 0
        self.tigers.remove(current)
        self.tigers.add(target)
        self.goats_captured += 1
        self.history.append(History(sid=sid, move="jump", piece=Player.TIGER.name, current=current, target=target, phase=self.phase.value, captured=mid))
        return True

    def move_tiger(self,current,target,sid=None, role=None):
        if (self.turn != Player.TIGER or self.winner or (role is not None and role != Player.TIGER.value)):
            return False
        moved = False
        if self.valid_normal_move(current,target):
            moved = self.tiger_normal_move(current,target,sid)
        elif self.valid_jump_move(current, target):
            moved = self.tiger_jump_move(current, target,sid)
        if moved:
            self._end_turn()
        return moved

    def are_tigers_trapped(self):
        for t in self.tigers:
            for neighbor in N[t]:
                # if kunai position khali xa vane from tigers position, then tiger abhi zinda he lol
                if self.is_empty(neighbor):
                    return False
            # jump garna pai raxa vane tiger aajhai zinda xa
            for (start, end), mid in J.items():
                if start == t and self.board[mid] == Player.GOAT.value and self.is_empty(end):
                    return False
        # Tiger abhi zinda he lolllll
        return True
    
    def check_winner(self):
        if self.goats_captured >= 5:
            self.winner = Player.TIGER
        elif self.are_tigers_trapped():
            self.winner = Player.GOAT

    def get_possible_moves(self, pos):
        moves = []
        for neighbor in N[pos]:
            if self.is_empty(neighbor):
                moves.append(neighbor)
        for (start, end), mid in J.items():
            if start == pos and self.board[mid] == Player.GOAT.value and self.is_empty(end):
                moves.append(end)
        return moves

    def get_history(self):
        return [
            {
                "player": move.sid,
                "piece": move.piece,
                "current": move.current,
                "target": move.target,
                "move_type": move.move,
                "captured": move.captured,
                "phase": move.phase
            }
            for move in self.history
        ]
    
    def get_state(self):
        return {
            "board": self.board,
            "turn": self.turn.value,
            "phase": self.phase.value,
            "goats_placed": self.goats_placed,
            "goats_captured": self.goats_captured,
            "winner": self.winner.value if self.winner else None,
            "history": self.get_history()
        }