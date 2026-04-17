import socketio
from src.server.models import *
import uvicorn
import uuid

sio = socketio.AsyncServer(cors_allowed_origins="*", async_mode="asgi")
app = socketio.ASGIApp(sio)
room = Room(room_id=str(uuid.uuid4()))

@sio.event
async def connect(sid, environ, auth):
    room.add_user(sid)
    await sio.enter_room(sid, room.room_id)
    await sio.emit("room_details", room.details, to=room.room_id)

@sio.event
async def disconnect(sid):
    room.remove_user(sid)
    await sio.emit("room_details", room.details, to=room.room_id)

@sio.event
async def place_goat(sid, data):
    print("GOT PLACE GOAT EVENT", data)
    target = data.get("target")
    role = room.get_user_by_sid(sid).role
    print("ROLE", role)
    room.engine.place_goat(target,sid,role)
    await sio.emit("room_details", room.details, to=room.room_id)

@sio.event
async def move_goat(sid, data):
    print("GOT MOVE GOAT EVENT", data)
    current = data.get("current")
    target = data.get("target")
    role = room.get_user_by_sid(sid).role
    room.engine.move_goat(current, target, sid, role)
    await sio.emit("room_details", room.details, to=room.room_id)

@sio.event
async def move_tiger(sid, data):
    print("GOT MOVE TIGER EVENT", data)
    print(room.details)
    current = data.get("current")
    target = data.get("target")
    role = room.get_user_by_sid(sid).role
    room.engine.move_tiger(current, target, sid, role)
    await sio.emit("room_details", room.details, to=room.room_id)

@sio.event
async def get_possible_moves(sid, data):
    pos = data.get("pos")
    moves = room.engine.get_possible_moves(pos)
    await sio.emit("possible_moves", {"pos": pos, "moves": moves}, to=sid)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 