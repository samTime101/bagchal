from enum import Enum

class Player(Enum):
    GOAT = 1
    TIGER = -1

class Phase(Enum):
    PLACEMENT = 1
    MOVEMENT = 2