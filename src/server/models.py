from dataclasses import dataclass
from typing import Dict
from src.engine.engine import Engine
from src.engine.utils.enums import *
import uuid

@dataclass
class User:
    sid: str
    role: int = None

class RoomManager:
    def __init__(self):
        self.rooms: Dict[str, Room] = {} # room_id: Room
        self.user_room_map: Dict[str, str] = {} # user_id: room_id

    def create_room(self) -> Room:
        room = Room(room_id=str(uuid.uuid4()))
        self.rooms[room.room_id] = room
        return room

    def find_or_create_room(self) -> Room:
        for room in self.rooms.values():
            if len(room.users) < room.max_users:
                return room
        return self.create_room()

    def add_user(self, sid: str) -> Room:
        room = self.find_or_create_room()
        if room.add_user(sid):
            self.user_room_map[sid] = room.room_id
        return room

    def remove_user(self, sid: str):
        room_id = self.user_room_map.get(sid)
        if not room_id:
            return None
        room = self.rooms.get(room_id)
        if not room:
            return None
        room.remove_user(sid)
        self.user_room_map.pop(sid, None)
        if len(room.users) == 0:
            self.rooms.pop(room_id)
        return room

    def get_room_by_sid(self, sid: str) -> Room | None:
        room_id = self.user_room_map.get(sid)
        if not room_id:
            return None
        return self.rooms.get(room_id)

class Room:
    def __init__(self, room_id: str):
        self.room_id = room_id
        self.users: Dict[str, User] = {}
        self.max_users = 2
        self.engine = Engine()

    def _assign_roles(self):
        if len(self.users) == 0:
            return
        sids = list(self.users.keys())
        if len(sids) >= 1:
            self.users[sids[0]].role = Player.GOAT.value #1
        if len(sids) >= 2:
            self.users[sids[1]].role = Player.TIGER.value #-1

    def add_user(self, sid: str):
        if len(self.users) >= self.max_users:
            return False
        self.users[sid] = User(sid=sid)
        self._assign_roles()
        return True

    def get_user_by_sid(self, sid: str) -> User | None:
        return self.users.get(sid)
    
    def remove_user(self, sid: str):
        self.users.pop(sid, None)
        self._assign_roles()

    def reset(self):
        self.engine = Engine()

    @property
    def details(self):
        return {
            "room_id": self.room_id,
            "user_count": len(self.users),
            "max_users": self.max_users,
            "users": [
                {
                    "sid": user.sid,
                    "role": user.role,
                }
                for user in self.users.values()
            ],
            "engine": self.engine.get_state(),
        }