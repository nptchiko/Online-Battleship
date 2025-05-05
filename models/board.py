from models.cell import Cell, CellState
from models.ship import Ship, Orientation
import random


class Board:
    """Represents the game board in the Battleship game."""

    def __init__(self, size=10):
        """Initialize a board with the specified size.

        Args:
            size (int): The size of the board (both width and height)
        """
        self.size = size
        self.grid = [[Cell(row, col) for col in range(size)]
                     for row in range(size)]
        self.ships = []
        self.shots_fired = 0
        self.hits = 0

    def place_ship(self, ship, row, col, orientation):
        """Place a ship on the board.

        Args:
            ship (Ship): The ship to place
            row (int): The starting row index
            col (int): The starting column index
            orientation (Orientation): The orientation of the ship

        Returns:
            bool: True if the ship was placed successfully, False otherwise
        """
        # Check if the ship can be placed at the specified position
        if not self._can_place_ship(ship.size, row, col, orientation):
            return False

        # Place the ship
        ship.place(row, col, orientation)
        coordinates = ship.get_coordinates()

        for r, c in coordinates:
            self.grid[r][c].place_ship(ship)

        self.ships.append(ship)
        return True

    def _can_place_ship(self, ship_size, row, col, orientation):
        """Check if a ship can be placed at the specified position.

        Args:
            ship_size (int): The size of the ship
            row (int): The starting row index
            col (int): The starting column index
            orientation (Orientation): The orientation of the ship

        Returns:
            bool: True if the ship can be placed, False otherwise
        """
        # Check if the ship would go out of bounds
        if orientation == Orientation.HORIZONTAL:
            if col + ship_size > self.size:
                return False
        else:  # VERTICAL
            if row + ship_size > self.size:
                return False

        # Check if the ship would overlap with another ship
        for i in range(ship_size):
            r, c = row, col
            if orientation == Orientation.HORIZONTAL:
                c += i
            else:  # VERTICAL
                r += i

            # Check if the cell already has a ship
            if self.grid[r][c].has_ship():
                return False

            # Check adjacent cells (optional, for spacing between ships)
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = r + dr, c + dc
                    if (0 <= nr < self.size and 0 <= nc < self.size and
                            (nr != r or nc != c) and self.grid[nr][nc].has_ship()):
                        return False

        return True

    def receive_shot(self, row, col):
        """Process a shot fired at the specified position.

        Args:
            row (int): The row index of the target cell
            col (int): The column index of the target cell

        Returns:
            tuple: (hit_success, ship_sunk, game_over)
        """
        if not (0 <= row < self.size and 0 <= col < self.size):
            return False, False, False

        cell = self.grid[row][col]
        if cell.is_attacked():
            return False, False, False

        self.shots_fired += 1
        hit, ship_sunk, _ = cell.receive_shot()

        if hit:
            self.hits += 1

        # Check if all ships are sunk
        game_over = all(ship.is_sunk() for ship in self.ships)

        return hit, ship_sunk, game_over

    def place_ships_randomly(self, ship_configs):
        """Place ships randomly on the board.

        Args:
            ship_configs (list): List of (size, name) tuples for ships to place

        Returns:
            bool: True if all ships were placed successfully, False otherwise
        """
        for size, name in ship_configs:
            ship = Ship(size, name)
            placed = False
            attempts = 0
            max_attempts = 100

            while not placed and attempts < max_attempts:
                row = random.randint(0, self.size - 1)
                col = random.randint(0, self.size - 1)
                orientation = random.choice(list(Orientation))

                placed = self.place_ship(ship, row, col, orientation)
                attempts += 1

            if not placed:
                # Remove any ships that were already placed
                self.reset()
                return False

        return True

    def reset(self):
        """Reset the board to its initial state."""
        self.grid = [[Cell(row, col) for col in range(self.size)]
                     for row in range(self.size)]
        self.ships = []
        self.shots_fired = 0
        self.hits = 0

    def get_cell(self, row, col):
        """Get the cell at the specified position.

        Args:
            row (int): The row index
            col (int): The column index

        Returns:
            Cell: The cell at the specified position
        """
        if 0 <= row < self.size and 0 <= col < self.size:
            return self.grid[row][col]
        return None

    def get_ship_at(self, row, col):
        """Get the ship at the specified position.

        Args:
            row (int): The row index
            col (int): The column index

        Returns:
            Ship: The ship at the specified position, or None if there is no ship
        """
        cell = self.get_cell(row, col)
        if cell and cell.has_ship():
            return cell.ship
        return None

    def get_all_cells(self):
        """Get all cells on the board.

        Returns:
            list: A flattened list of all cells
        """
        return [cell for row in self.grid for cell in row]

    def get_hit_ratio(self):
        """Calculate the hit ratio.

        Returns:
            float: The ratio of hits to shots fired, or 0 if no shots have been fired
        """
        if self.shots_fired == 0:
            return 0
        return self.hits / self.shots_fired

    def __str__(self):
        """String representation of the board.

        Returns:
            str: A string representing the board
        """
        result = "  " + " ".join(str(i) for i in range(self.size)) + "\n"
        for i, row in enumerate(self.grid):
            result += f"{i} " + " ".join(str(cell) for cell in row) + "\n"
        return result
