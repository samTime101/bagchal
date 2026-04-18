import socketio
from src.server.models import *
import uvicorn

sio = socketio.AsyncServer(cors_allowed_origins="*", async_mode="asgi")
app = socketio.ASGIApp(sio)
room_manager = RoomManager()

@sio.event
async def connect(sid, environ, auth):
    room_id = auth.get("room_id") if auth else None

    if room_id == "lobby":
        await sio.enter_room(sid, "lobby")
        await sio.emit("room_list", room_manager.room_list(), to=sid)
        return

    room = room_manager.add_user(sid, room_id)
    await sio.enter_room(sid, room.room_id)
    await sio.emit("room_details", room.details, to=room.room_id)
    await sio.emit("room_list", room_manager.room_list(), to="lobby")

@sio.event
async def disconnect(sid):
    room = room_manager.remove_user(sid)
    if room:
        await sio.emit("room_details", room.details, to=room.room_id)
        await sio.emit("room_list", room_manager.room_list(), to="lobby")

@sio.event
async def place_goat(sid, data):
    print("GOT PLACE GOAT EVENT", data)
    room = room_manager.get_room_by_sid(sid)
    if not room:
        return
    target = data.get("target")
    user = room.get_user_by_sid(sid)
    if not user or user.role != Player.GOAT.value:
        return
    print("ROLE", user.role)
    if room.engine.place_goat(target,sid,user.role):
        await sio.emit("room_details", room.details, to=room.room_id)

@sio.event
async def move_goat(sid, data):
    print("GOT MOVE GOAT EVENT", data)
    room = room_manager.get_room_by_sid(sid)
    if not room:
        return
    current = data.get("current")
    target = data.get("target")
    user = room.get_user_by_sid(sid)
    if not user or user.role != Player.GOAT.value:
        return
    if room.engine.move_goat(current, target, sid, user.role):
        await sio.emit("room_details", room.details, to=room.room_id)

@sio.event
async def move_tiger(sid, data):
    print("GOT MOVE TIGER EVENT", data)
    room = room_manager.get_room_by_sid(sid)
    if not room:
        return
    print(room.details)
    current = data.get("current")
    target = data.get("target")
    user = room.get_user_by_sid(sid)
    if not user or user.role != Player.TIGER.value:
        return
    if room.engine.move_tiger(current, target, sid, user.role):
        await sio.emit("room_details", room.details, to=room.room_id)

@sio.event
async def get_possible_moves(sid, data):
    room = room_manager.get_room_by_sid(sid)
    if not room:
        return
    pos = data.get("pos")
    moves = room.engine.get_possible_moves(pos)
    await sio.emit("possible_moves", {"pos": pos, "moves": moves}, to=sid)

# SHITTY CODE
@sio.event
async def restart_game(sid):
    room = room_manager.get_room_by_sid(sid)
    if not room:
        return
    user = room.get_user_by_sid(sid)
    if room.restart(user.sid):
        await sio.emit("room_details", room.details, to=room.room_id)

@sio.event
async def room_list(sid):
    await sio.emit("room_list", room_manager.room_list(), to=sid)

@sio.event
async def room_detail(sid):
    room = room_manager.get_room_by_sid(sid)
    if not room:
        return
    await sio.emit("room_details", room.details, to=sid)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 