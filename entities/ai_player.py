import random
from player import Player
from ship import Ship
from direction import Direction


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
