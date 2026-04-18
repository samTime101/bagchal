import uuid
from src.server.models import Room, RoomManager

async def emit_to_players(sio,room: Room, event: str):
    data = room.chat
    print("EMITTING CHAT", data)
    for sid in room.players:
        await sio.emit(event, data, to=sid)

def _parse_auth_data(auth: dict | None) -> tuple[uuid.UUID | None, str | None]:
    if not auth:
        return None, None
    uid_str = auth.get("uid")
    room_id = auth.get("room_id")
    uid = None
    if uid_str:
        try:
            uid = uuid.UUID(uid_str)
        except ValueError:
            pass 
    return uid, room_id

async def _handle_lobby_connection(sio, sid: str, room_manager: RoomManager):
    await sio.enter_room(sid, "lobby")
    await sio.emit("room_list", room_manager.room_list(), to=sid)

def _resolve_user_and_room(sio, sid: str, uid: uuid.UUID | None, room_id: str | None, room_manager: RoomManager) -> Room:
    room, user = room_manager.get_room_and_user_by_uid(uid) if uid else (None, None)    
    if room and user:
        room.replace_sid(user.sid, sid)
        return room
    return room_manager.add_user(sid, room_id)
