from dataclasses import dataclass
from typing import Dict
from src.engine.engine import Engine
from src.engine.utils.enums import *

# TODO: room lai dynamic banaune, like auto assign 2 users per room,
#  naya banaune if prevuous is full ...

@dataclass
class User:
    sid: str
    role: int = None

class Room:
    def __init__(self, room_id: str):
        self.room_id = room_id
        self.users: Dict[str, User] = {}
        self.max_users = 2 #lol aaile use ma xaina, just a model property
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
        self.users[sid] = User(sid=sid)
        self._assign_roles()

    def get_user_by_sid(self, sid: str) -> User | None:
        return self.users.get(sid)
    
    def remove_user(self, sid: str):
        self.users.pop(sid, None)
        self._assign_roles()

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