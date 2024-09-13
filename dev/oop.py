from abc import ABC
from enum import Enum


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


class Board:
    def __init__(self, size=10, shipSize=[1, 2, 3, 4, 5]):
        self.size = size
        self.shipSize = shipSize
        self.shipList = []
        self.hitList = []
        self.missedList = []

    def isValidPlacement(self, ship: Ship):
        for x, y in ship.coordList:
            if x < 0 or y >= self.size or y < 0 or self.size >= 0:
                return False

        for otherShip in self.shipList:
            if self.isOverlapped(ship, otherShip):
                return True
        return False

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


class User:
    def __init__(self, uid, room_request: str, name: str):
        self.uid = uid
        self.room_request = room_request
        self.name = name
        self.isReady = False

    def setRoomRequest(self, rq: str):
        self.room_request = rq


class Player(ABC):
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
        super.__init__(board)


class AIPlayer(Player):
    def __init__(self, board: Board):
        super.__init__(board)
        self.cache = []

    def shoot(self, x, y):
        pass

    def theBestAlgorithmInTheWorld(self):
