from enum import Enum
import time
import random


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

    @property
    def coordList(self):
        x, y = self.coord

        if self.dir == Direction.NORTH:
            return [(x, y - i) for i in range(0, self.len)]

        elif self.dir == Direction.WEST:
            return [(x - i, y) for i in range(0, self.len)]

        elif self.dir == Direction.SOUTH:
            return [(x, y + i) for i in range(0, self.len)]

        elif self.dir == Direction.EAST:
            return [(x + i, y) for i in range(0, self.len)]

    def rotate(self):
        self.dir = self.dir.next

    def __str__(self):
        return "Location: {}, len: {}, dir: {}\n".format(
            self.coordList, self.len, self.dir
        )

    def __repr__(self):
        return str(self)


class Board:
    def __init__(self, size=10, shipSize=[1, 2, 3, 4, 5]):
        self.size = size
        self.shipSize = shipSize
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
        else:
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
    def __init__(self, uid, room_request: str, name: str):
        self.uid = uid
        self.room_request = room_request
        self.name = name
        self.isReady = False

    def setRoomRequest(self, rq: str):
        self.room_request = rq

    def setReady(self, val: bool):
        self.isReady = val

    def __repr__(self):
        return "uid: {}, room_request: {}, name: {}\n".format(
            self.uid, self.room_request, self.name
        )


class Player:
    def __init__(self, board: Board):
        self.board = board
        self.user = None

    def setUser(self, user: User):
        self.user = user

    def shoot(self, x, y):
        # take input
        # example
        if self.board.isValidTarget(x, y):
            for ship in self.board.shipList:
                if (x, y) in ship.coordList:
                    self.board.hitList.append((x, y))
                    return 1

            self.board.missedList.append((x, y))
            return 0

        return -1


class PlayerUser(Player):
    def __init__(self, board: Board):
        super().__init__(board)


class AIPlayer(Player):
    def __init__(self, board: Board):
        super().__init__(board)
        self.cache: list = []

    def shoot(self):
        coord = self.theBestAlgorithmInTheWorld()
        ship: Ship
        for ship in self.board.shipList:
            if coord in ship.coordList:
                self.cache.append(coord)
                self.board.hitList.append(coord)
                return 1
        self.board.missedList.append(coord)
        return 0

    def theBestAlgorithmInTheWorld(self):
        print(self.cache)
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
        while self.board.isValidTarget(x, y) == False:
            x = random.randint(0, self.board.size - 1)
            y = random.randint(0, self.board.size - 1)

        return x, y


class Room:
    def __init__(self):
        self.userInRoom: list = []
        self.id: str = ""
        self.turn: int = 0

    def setId(self, id: str):
        self.id = id

    def addUser(self, user: User):
        self.userInRoom.append(user)

    def removeUser(self, uid):
        user: User
        for user in self.userInRoom:
            if user.uid == uid:
                self.userInRoom.remove(user)
                return True
        return False

    def getNumberOfUser(self):
        return len(self.userInRoom)

    def checkAllReady(self):
        user: User
        for user in self.userInRoom:
            if not user.isReady():
                return False
        return True

    def checkRoomAvailable(self):
        return len(self.userInRoom) < 2

    def swapTurn(self):
        return (self.turn + 1) % 2

    def startNewRound(self):
        user: User
        for user in self.userInRoom:
            user.setReady(False)

    def __str__(self):
        return "id: {}, userInRoom: {}".format(self.id, self.userInRoom)


# ship = Ship(4, 4, 3, Direction.NORTH)
# board = Board()
# board.addShip(ship)
# board.addShip(Ship(5, 5, 5, Direction.NORTH))
# print(board.printBoard())
# board.addShip(Ship(2, 7, 5, Direction.EAST))
# player = AIPlayer(board)
# player.setUser(User("001", "1", "bot"))
#
# for i in range(1, 50):
#     print(i)
#     player.shoot()
#     player.board.printBoard()
#     time.sleep(1)


user1 = User("123", "1", "Lucy")
user2 = User("234", "1", "John")

room = Room()
room.addUser(user1)
room.addUser(user2)