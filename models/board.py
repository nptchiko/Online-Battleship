from models.cell import Cell, CellState
from models.ship import Ship, Orientation
import random


class Board:

    def __init__(self, size=10):

        self.size = size
        self.grid = [[Cell(row, col) for col in range(size)]
                     for row in range(size)]
        self.ships = []
        self.shots_fired = 0
        self.hits = 0

    def place_ship(self, ship, row, col, orientation):
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
        # Check if the ship would go out of bounds
        if orientation == Orientation.HORIZONTAL:
            if col + ship_size > self.size:
                return False
        else:  # VERTICAL
            if row + ship_size > self.size:
                return False

        for i in range(ship_size):
            r, c = row, col
            if orientation == Orientation.HORIZONTAL:
                c += i
            else:  # VERTICAL
                r += i

            # Check if the cell already has a ship
            if self.grid[r][c].has_ship():
                return False
        return True

    def receive_shot(self, row, col):
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
        self.reset()
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

        self.grid = [[Cell(row, col) for col in range(self.size)]
                     for row in range(self.size)]
        self.ships = []
        self.shots_fired = 0
        self.hits = 0

    def get_cell(self, row, col):

        if 0 <= row < self.size and 0 <= col < self.size:
            return self.grid[row][col]
        return None

    def get_ship_at(self, row, col):
        cell = self.get_cell(row, col)
        if cell and cell.has_ship():
            return cell.ship
        return None

    def get_all_cells(self):
        return [cell for row in self.grid for cell in row]

    def get_hit_ratio(self):
        if self.shots_fired == 0:
            return 0
        return self.hits / self.shots_fired

    def __str__(self):
        result = "  " + " ".join(str(i) for i in range(self.size)) + "\n"
        for i, row in enumerate(self.grid):
            result += f"{i} " + " ".join(str(cell) for cell in row) + "\n"
        return result
