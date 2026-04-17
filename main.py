from engine.engine import Engine

engine = Engine()
print(engine.board)
print(engine.board[1])
print(engine.get_piece())
print(engine.place_goat(1))
print(engine.board)
print(engine.turn)
print(engine.goats_placed)
print(engine.move_tiger(0,2))
print(engine.board)
print(engine.goats_captured)