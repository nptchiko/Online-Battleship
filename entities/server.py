from typing import Any
from user import User
from room import Room


class Server:
    def __init__(self, onlineUser: dict = {}, onlineRoom: dict = {}):
        self.onlineUser: dict[Any, User] = onlineUser
        self.onlineRoom: dict[Any, Room] = onlineRoom

    def addUser(self, uid):
        self.onlineUser[uid] = User(uid)

    def addRoom(self, user: User):
        room: Room = Room(user.room_request)
        room.accept(user)
        self.onlineRoom[user.room_request] = room

    def delUser(self, request_id):
        self.onlineUser.pop(request_id)

    def delRoom(self, room_id):
        self.onlineRoom.pop(room_id)
