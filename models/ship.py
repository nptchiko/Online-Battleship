from enum import Enum


class Orientation(Enum):

    HORIZONTAL = 0
    VERTICAL = 1


class Ship:

    def __init__(self, size, name):

        self.size = size
        self.name = name
        self.hits = 0
        self.orientation = Orientation.HORIZONTAL
        self.row = None
        self.col = None
        self.is_placed = False

    def place(self, row, col, orientation):
        self.row = row
        self.col = col
        self.orientation = orientation
        self.is_placed = True

    def hit(self):
        self.hits += 1
        return self.is_sunk()

    def is_sunk(self):
        return self.hits >= self.size

    def get_coordinates(self):
        if not self.is_placed:
            return []

        coordinates = []
        for i in range(self.size):
            if self.orientation == Orientation.HORIZONTAL:
                coordinates.append((self.row, self.col + i))
            else:  # VERTICAL
                coordinates.append((self.row + i, self.col))

        return coordinates

    def __str__(self):
        status = "sunk" if self.is_sunk() else f"{self.hits}/{self.size} hits"
        position = f"at ({self.row}, {
            self.col})" if self.is_placed else "not placed"
        orientation = "horizontal" if self.orientation == Orientation.HORIZONTAL else "vertical"
        return f"{self.name} ({self.size}) {position}, {orientation}, {status}"
