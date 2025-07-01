from typing import Any
from user import User
from battleship import BattleShip


class Room:
    def __init__(self, id: str):
        self.userInRoom: dict[Any, User] = {}
        self.id: str = id
        self.game: BattleShip

    def accept(self, user: User):
        if self.isRoomAvailable():
            self.userInRoom[user.uid] = user
            return True
        return False

    def kick(self, uid):
        if self.userInRoom.get(uid) is None:
            return False

        self.userInRoom.pop(uid)
        return True

    def checkAllReady(self):
        for key in self.userInRoom.keys():
            if not self.userInRoom[key].isReady:
                return False
        return True

    def isRoomAvailable(self):
        return len(self.userInRoom) < 2

    def startGame(self):
        self.game = BattleShip(self.userInRoom)

    def getNumberOfUser(self):
        return len(self.userInRoom)

    def startNewRound(self):
        for key in self.userInRoom.keys():
            self.userInRoom[key].isReady = False

    def __str__(self):
        return "id: {}, userInRoom: {}".format(self.id, self.userInRoom)
