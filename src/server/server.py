import socketio
from src.server.models import *
import uvicorn
import uuid

sio = socketio.AsyncServer(cors_allowed_origins="*", async_mode="asgi")
app = socketio.ASGIApp(sio)
room_manager = RoomManager()

@sio.event
async def connect(sid, environ, auth):
    room = room_manager.add_user(sid)
    await sio.enter_room(sid, room.room_id)
    await sio.emit("room_details", room.details, to=room.room_id)

@sio.event
async def disconnect(sid):
    room = room_manager.remove_user(sid)
    if room:
        await sio.emit("room_details", room.details, to=room.room_id)

@sio.event
async def place_goat(sid, data):
    print("GOT PLACE GOAT EVENT", data)
    room = room_manager.get_room_by_sid(sid)
    if not room:
        return
    target = data.get("target")
    role = room.get_user_by_sid(sid).role
    print("ROLE", role)
    room.engine.place_goat(target,sid,role)
    await sio.emit("room_details", room.details, to=room.room_id)

@sio.event
async def move_goat(sid, data):
    print("GOT MOVE GOAT EVENT", data)
    room = room_manager.get_room_by_sid(sid)
    if not room:
        return
    current = data.get("current")
    target = data.get("target")
    role = room.get_user_by_sid(sid).role
    room.engine.move_goat(current, target, sid, role)
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
    role = room.get_user_by_sid(sid).role
    room.engine.move_tiger(current, target, sid, role)
    await sio.emit("room_details", room.details, to=room.room_id)

@sio.event
async def get_possible_moves(sid, data):
    room = room_manager.get_room_by_sid(sid)
    if not room:
        return
    pos = data.get("pos")
    moves = room.engine.get_possible_moves(pos)
    await sio.emit("possible_moves", {"pos": pos, "moves": moves}, to=sid)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 