from typing import Any
from game import Game
from player_user import PlayerUser
from ai_player import AIPlayer
from ship import Ship
from direction import Direction


class BattleShip(Game):
    def __init__(self, userInRoom: dict):
        super().__init__()
        for key in userInRoom.keys():
            self.players[key] = PlayerUser(userInRoom[key])
            self.keys.append(key)

        if len(userInRoom) < 2:
            self.players["bot"] = AIPlayer()
            self.keys.append("bot")
        self.nextTurn()

    def placeShip(self, data: dict, uid):
        for key in data.keys():
            info: dict[str, Any] = data[key]
            len: int = info["len"]
            x: int = info["coord"]["x"]
            y: int = info["coord"]["y"]
            dir: int = info["dir"]
            ship = Ship(x, y, len, Direction(dir))

            if not self.players[uid].board.addShip(ship):
                return False

        return True

    def isCurrentPlayerWin(self, uid):
        return len(self.players[uid].board.hitList) >= 15

    def checkAllReady(self):
        for key in self.players.keys():
            if not self.players[key].placedShip:
                return False
        return True
