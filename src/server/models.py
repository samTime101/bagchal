from dataclasses import dataclass, field
from typing import Dict, List, Optional
from src.engine.engine import Engine
from src.engine.utils.enums import *
import uuid


# @TODO: reset logic vanda pani, 
# some features which i saw on chess.com
# 1. restart match
# 2. resign option
# 3. draw offer
# 4. draw lai kasari handle garne ra if draw hunxa ki hudaina bagchal ma tyo ni check garne lol malai taha xaina if draw is possible or not

@dataclass
class User:
    sid: str
    uid: uuid.UUID = field(default_factory=uuid.uuid4)
    role: int = None

@dataclass
class ChatMessage:
    message: str
    time: float
    sender: Optional[User] = None

class RoomManager:
    def __init__(self):
        self.rooms: Dict[str, Room] = {} # room_id: Room
        self.user_room_map: Dict[str, str] = {} # user_id: room_id
        self.connected_users = {} # sid -> uid

    def create_room(self) -> Room:
        room = Room(room_id=str(uuid.uuid4()))
        self.rooms[room.room_id] = room
        return room

    def get_total_online(self) -> int:
        return len(set(uid for uid in self.connected_users.values() if uid))

    def find_or_create_room(self) -> Room:
        for room in self.rooms.values():
            if not room.is_full:
                return room
        return self.create_room()

    def add_user(self, sid: str, room_id: str = None) -> Optional[Room]:
        if sid in self.user_room_map:
            self.remove_user(sid)
        room = None
        if room_id and room_id in self.rooms:
            room = self.rooms[room_id]
        if room is None:
            room = self.find_or_create_room()
        if room.add_user(sid):
            self.user_room_map[sid] = room.room_id
            return room
        return None

    def remove_user(self, sid: str):
        room_id = self.user_room_map.get(sid)
        if not room_id:
            return None
        room = self.rooms.get(room_id)
        if not room:
            return None
        if sid not in room.users:
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
    
    def get_room_and_user_by_uid(self, uid: uuid.UUID):
        for room in self.rooms.values():
            sid = room.uid_sid_map.get(uid)
            if sid:
                return room, room.users.get(sid)
        return None, None

    def room_list(self):
        return {
            room_id: {
                "user_count": len(room.users),
                "max_players": room.max_players,
                "users": [
                    {
                        "sid": user.sid,
                        "role": user.role,
                    }
                    for user in room.users.values()
                ],
            }
            for room_id, room in self.rooms.items()
        }

class Room:
    def __init__(self, room_id: str):
        self.room_id = room_id
        self.users: Dict[str, User] = {} # sid: User
        self.uid_sid_map: Dict[uuid.UUID, str] = {} # uid: sid
        self.max_players = 2
        self.engine = Engine()
        self.chat_history: List[ChatMessage] = []

    @property
    def players(self):
        return {sid: user for sid, user in self.users.items() if user.role is not None}
    
    @property
    def spectators(self):
        return {sid: user for sid, user in self.users.items() if user.role is None}

    @property
    def is_full(self):
        return len(self.players) >= self.max_players

    def __get_available_role(self):
        assigned_roles = {user.role for user in self.users.values() if user.role is not None}
        if Player.GOAT.value not in assigned_roles:
            return Player.GOAT.value
        if Player.TIGER.value not in assigned_roles:
            return Player.TIGER.value
        return None

    def add_user(self, sid: str, uuid: uuid.UUID = None) -> bool:
        if sid in self.users:
            return False
        role = self.__get_available_role()
        self.users[sid] = User(sid=sid, role=role, uid=uuid)
        if uuid:
            self.uid_sid_map[uuid] = sid
        return True
    
    def replace_sid(self, old_sid: str, new_sid: str):
        user = self.users.pop(old_sid, None)
        if not user:
            return

        user.sid = new_sid
        self.users[new_sid] = user

        if user.uid:
            self.uid_sid_map[user.uid] = new_sid
    
    def remove_user(self, sid: str):
        user = self.users.pop(sid, None)
        if user and user.uid:
            self.uid_sid_map.pop(user.uid, None)

    def restart(self, sid: str = None) -> bool:
        user = self.users.get(sid)
        if not user or user.role is None or self.engine.winner is None:
            return False
        self.engine = Engine()
        return True


    @property
    def details(self):
        return {
            "room_id": self.room_id,
            "user_count": len(self.users),
            "max_players": self.max_players,
            "spectators": [
                {
                    "uid": str(user.uid),
                    "sid": user.sid,
                }
                for user in self.spectators.values()
            ],
            "players": [
                {
                    "uid": str(user.uid),
                    "sid": user.sid,
                    "role": user.role,
                }
                for user in self.players.values()
            ],
            "engine": self.engine.get_state(),
        }
    
    @property
    def chat(self):
        return [
            {
                "sender": {
                    "uid": str(msg.sender.uid) if msg.sender else None,
                    "sid": msg.sender.sid if msg.sender else None,
                    "role": msg.sender.role if msg.sender else None,
                },
                "message": msg.message,
                "time": msg.time,
            }
            for msg in self.chat_history
        ]