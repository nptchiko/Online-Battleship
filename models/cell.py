from enum import Enum

class CellState(Enum):
    """Enum representing the possible states of a cell on the board."""
    EMPTY = 0
    SHIP = 1
    HIT = 2
    MISS = 3

class Cell:
    """Represents a single cell on the game board."""
    
    def __init__(self, row, col):
        """Initialize a cell with its position and default state.
        
        Args:
            row (int): The row index of the cell
            col (int): The column index of the cell
        """
        self.row = row
        self.col = col
        self.state = CellState.EMPTY
        self.ship = None
    
    def place_ship(self, ship):
        """Place a ship on this cell.
        
        Args:
            ship: The ship object to place on this cell
        """
        self.ship = ship
        self.state = CellState.SHIP
    
    def receive_shot(self):
        """Process a shot fired at this cell.
        
        Returns:
            tuple: (hit_success, ship_sunk, game_over)
        """
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
        """Check if this cell has been attacked.
        
        Returns:
            bool: True if the cell has been hit or missed, False otherwise
        """
        return self.state == CellState.HIT or self.state == CellState.MISS
    
    def has_ship(self):
        """Check if this cell contains a ship.
        
        Returns:
            bool: True if the cell contains a ship, False otherwise
        """
        return self.state == CellState.SHIP or (self.state == CellState.HIT and self.ship is not None)
    
    def __str__(self):
        """String representation of the cell.
        
        Returns:
            str: A character representing the cell state
        """
        if self.state == CellState.EMPTY:
            return "·"
        elif self.state == CellState.SHIP:
            return "S"
        elif self.state == CellState.HIT:
            return "X"
        elif self.state == CellState.MISS:
            return "O"
        return "?"
