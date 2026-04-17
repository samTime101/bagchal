from src.engine.engine import Engine
from src.engine.utils.enums import Player, Phase

engine = Engine()
print(engine.board)
print(engine.board[1])
print(engine.place_goat(1,role=Player.GOAT.value))
print(engine.board)
print(engine.turn)
print(engine.goats_placed)
print(engine.move_tiger(0,2,role=Player.TIGER.value))
print(engine.board)
print(engine.goats_captured)
print(engine.history)
print("==")
print(engine.get_state())
