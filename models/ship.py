from enum import Enum


class Orientation(Enum):
    """Enum representing the possible orientations of a ship."""
    HORIZONTAL = 0
    VERTICAL = 1


class Ship:
    """Represents a ship in the Battleship game."""

    def __init__(self, size, name):
        """Initialize a ship with its size and name.

        Args:
            size (int): The size of the ship (number of cells it occupies)
            name (str): The name of the ship (e.g., "Carrier", "Battleship")
        """
        self.size = size
        self.name = name
        self.hits = 0
        self.orientation = Orientation.HORIZONTAL
        self.row = None
        self.col = None
        self.is_placed = False

    def place(self, row, col, orientation):
        """Place the ship on the board.

        Args:
            row (int): The starting row index
            col (int): The starting column index
            orientation (Orientation): The orientation of the ship
        """
        self.row = row
        self.col = col
        self.orientation = orientation
        self.is_placed = True

    def hit(self):
        """Register a hit on the ship.

        Returns:
            bool: True if the ship is sunk after this hit, False otherwise
        """
        self.hits += 1
        return self.is_sunk()

    def is_sunk(self):
        """Check if the ship is sunk.

        Returns:
            bool: True if the ship has been hit as many times as its size
        """
        return self.hits >= self.size

    def get_coordinates(self):
        """Get all coordinates occupied by the ship.

        Returns:
            list: List of (row, col) tuples representing the ship's coordinates
        """
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
        """String representation of the ship.

        Returns:
            str: A string describing the ship
        """
        status = "sunk" if self.is_sunk() else f"{self.hits}/{self.size} hits"
        position = f"at ({self.row}, {
            self.col})" if self.is_placed else "not placed"
        orientation = "horizontal" if self.orientation == Orientation.HORIZONTAL else "vertical"
        return f"{self.name} ({self.size}) {position}, {orientation}, {status}"
