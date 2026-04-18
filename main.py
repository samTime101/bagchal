from src.engine.engine import Engine
from src.engine.utils.enums import Player, Phase
from src.server.models import RoomManager, Room, User

# engine = Engine()
# print(engine.board)
# print(engine.board[1])
# print(engine.place_goat(1,role=Player.GOAT.value))
# print(engine.board)
# print(engine.turn)
# print(engine.goats_placed)
# print(engine.move_tiger(0,2,role=Player.TIGER.value))
# print(engine.board)
# print(engine.goats_captured)
# print(engine.history)
# print("==")
# print(engine.get_state())

room_manager = RoomManager()
room = room_manager.find_or_create_room()


print(room.room_id)
room.add_user("sid1")
room.add_user("sid2")
room.add_user("sid3")
print(len(room.users))

room = room_manager.rooms.get(room.room_id)
print(room.details)
