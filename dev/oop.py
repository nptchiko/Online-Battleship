from enum import Enum
import random
from typing import Any


class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    @property
    def next(self):
        return Direction((self.value + 1) % 4)


class Ship:
    def __init__(self, x, y, len, d: Direction):
        self.coord = (x, y)
        self.len = len
        self.dir = d
        self.coordList: list[tuple] = []

        if self.dir == Direction.NORTH:
            self.coordList = [(x, y - i) for i in range(0, self.len)]

        elif self.dir == Direction.WEST:
            self.coordList = [(x - i, y) for i in range(0, self.len)]

        elif self.dir == Direction.SOUTH:
            self.coordList = [(x, y + i) for i in range(0, self.len)]

        elif self.dir == Direction.EAST:
            self.coordList = [(x + i, y) for i in range(0, self.len)]

    def rotate(self):
        self.dir = self.dir.next

    def __str__(self):
        return "Location: :{}, len: {}, dir: {}\n".format(
            self.coordList, self.len, self.dir
        )

    def __repr__(self):
        return str(self)


class Board:
    def __init__(self, size=10):
        self.size = size
        self.shipSize: list = []
        self.shipList: list = []
        self.hitList: list = []
        self.missedList: list = []

    def isValidPlacement(self, ship: Ship):
        for x, y in ship.coordList:
            if x < 0 or y >= self.size or y < 0 or x >= self.size:
                return False

        for otherShip in self.shipList:
            if self.isOverlapped(ship, otherShip):
                return False
        return True

    def isOverlapped(self, sh1: Ship, sh2: Ship):
        for s1 in sh1.coordList:
            for s2 in sh2.coordList:
                if s1 == s2:
                    return True
        return False

    def addShip(self, ship: Ship):
        if self.isValidPlacement(ship):
            self.shipList.append(ship)
            return True
        return False

    def removeShip(self, ship: Ship):
        self.shipList.remove(ship)

    def getShip(self, x, y):
        for ship in self.shipList:
            if (x, y) in ship.coordList:
                return ship

        return None

    def isValidTarget(self, x, y):
        if x < 0 or y < 0 or x >= self.size or y >= self.size:
            return False

        for coord in self.missedList + self.hitList:
            if (x, y) == coord:
                return False

        return True

    def __str__(self):
        return "size: {}, shipList: {}".format(self.size, self.shipList)

    def printBoard(self):
        tile = [[" " for i in range(self.size)] for i in range(self.size)]
        ship: Ship
        for ship in self.shipList:
            cell = ship.coordList
            for x, y in cell:
                tile[y][x] = "S"

        if self.missedList != []:
            for x, y in self.missedList:
                tile[y][x] = "M"
        if self.hitList != []:
            for cell in self.hitList:
                x, y = cell
                tile[y][x] = "H"

        for row in tile:
            print(row)


class User:
    def __init__(self, uid, name: str = ""):
        self.uid = uid
        self.name: str = name
        self.isReady: bool = False
        self.room_request: str = ""

    # def setIsAvailable(self, val: bool):
    #     self.isInRoom = val
    #
    # def IsAvailable(self):
    #     return self.isInRoom
    #
    def setRoomRequest(self, rq: str):
        self.room_request = rq

    def __repr__(self):
        return "uid: {}, room: {},name: {}\n".format(
            self.uid, self.room_request, self.name
        )


class Player:
    def __init__(self):
        self.board = Board()
        self.placedShip: bool = False

    def isHit(self, coord: tuple):
        for ship in self.board.shipList:
            if coord in ship.coordList:
                return True
        return False

    def shoot(self, player, coord: tuple):
        result: bool = player.isHit(coord)

        if result:
            self.board.hitList.append(coord)
        else:
            self.board.missedList.append(coord)
        return {"coord": coord, "result": result}


class PlayerUser(Player):
    def __init__(self, user: User):
        super().__init__()
        self.user = user

    def __str__(self):
        return "{}".format(self.user.name)


class AIPlayer(Player):
    def __init__(self, cache: list = []):
        super().__init__()
        self.cache: list[tuple] = cache
        self.placedShip = True

        lens: list = [1, 2, 3, 4, 5]

        while lens != []:
            len: int = lens[0]
            x: int = random.randint(0, 9)
            y: int = random.randint(0, 9)
            dir = Direction(random.randint(0, 3))
            ship = Ship(x, y, len, dir)

            if self.board.isValidPlacement(ship):
                self.board.addShip(ship)
                lens.pop(0)

    def shoot(self, player: Player, coord: tuple):
        result = super().shoot(player, coord)

        if result["result"]:
            self.cache.append(coord)
        return result

    def theBestAlgorithmInTheWorld(self):
        # print(self.cache)
        while self.cache != []:
            cell = self.cache[0]
            if self.board.isValidTarget(cell[0] + 1, cell[1]):
                return (cell[0] + 1, cell[1])

            if self.board.isValidTarget(cell[0] - 1, cell[1]):
                return (cell[0] - 1, cell[1])

            if self.board.isValidTarget(cell[0], cell[1] + 1):
                return (cell[0], cell[1] + 1)

            if self.board.isValidTarget(cell[0], cell[1] - 1):
                return (cell[0], cell[1] - 1)
            self.cache.pop(0)

        return self.takeRandom()

    def takeRandom(self):
        x = 0
        y = 0
        while not self.board.isValidTarget(x, y):
            x = random.randint(0, self.board.size - 1)
            y = random.randint(0, self.board.size - 1)

        return (x, y)

    def __str__(self):
        return "bot"


class Room:
    def __init__(self, id: str):
        self.userInRoom: dict[Any, User] = {}
        self.id: str = id
        self.game: Game

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


class Game:
    def __init__(self):
        self.players: dict[Any, Player] = {}
        self.keys: list = []
        self.turn = None

    def nextTurn(self):
        self.turn = self.keys.pop(0)
        self.keys.append(self.turn)
        return self.turn


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


# ship = Ship(4, 4, 3, Direction.NORTH)
#
# player = AIPlayer()
#
# player.board.addShip(ship)
# player.board.addShip(Ship(5, 5, 5, Direction.NORTH))
# player.board.addShip(Ship(2, 7, 5, Direction.EAST))
#
# for i in range(1, 50):
#     print(i)
#     player.shoot()
#     player.board.printBoard()
#     time.sleep(1)


# user1 = User("123", "1", "Lucy")
# user2 = User("234", "1", "John")
#
# room = Room()
# room.addUser(user1)
# room.addUser(user2)
#
# print(room def autoPlaceShip(self):)
