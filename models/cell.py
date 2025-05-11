from enum import Enum


class CellState(Enum):

    EMPTY = 0
    SHIP = 1
    HIT = 2
    MISS = 3


class Cell:

    def __init__(self, row, col):

        self.row = row
        self.col = col
        self.state = CellState.EMPTY
        self.ship = None

    def place_ship(self, ship):
        self.ship = ship
        self.state = CellState.SHIP

    def receive_shot(self):
        if self.state == CellState.EMPTY:
            self.state = CellState.MISS
            return False, False, False

        elif self.state == CellState.SHIP:
            self.state = CellState.HIT
            if self.ship:
                self.ship.hit()
                ship_sunk = self.ship.is_sunk()
                return True, ship_sunk, False
            return True, False, False

        # Already hit or missed
        return False, False, False

    def is_attacked(self):
        return self.state == CellState.HIT or self.state == CellState.MISS

    def has_ship(self):
        return self.state == CellState.SHIP or (self.state == CellState.HIT and self.ship is not None)

    def __str__(self):
        if self.state == CellState.EMPTY:
            return "·"
        elif self.state == CellState.SHIP:
            return "S"
        elif self.state == CellState.HIT:
            return "X"
        elif self.state == CellState.MISS:
            return "O"
        return "?"
