from ship import Ship


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
