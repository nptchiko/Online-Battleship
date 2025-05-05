from abc import ABC, abstractmethod
import random
from models.cell import CellState


class AIStrategy(ABC):
    """Abstract base class for AI strategies in Battleship game."""

    def __init__(self, board_size=10):
        """Initialize the AI strategy.

        Args:
            board_size (int): The size of the game board
        """
        self.board_size = board_size
        self.name = "Base AI"
        self.description = "Base AI strategy"

    @abstractmethod
    def get_move(self, opponent_board):
        """Get the next move for the AI.

        Args:
            opponent_board: The opponent's board

        Returns:
            tuple: (row, col) coordinates for the next shot
        """
        pass

    @abstractmethod
    def notify_result(self, row, col, hit, ship_sunk, game_over):
        """Update the AI with the result of its last move.

        Args:
            row (int): The row index of the last shot
            col (int): The column index of the last shot
            hit (bool): Whether the shot was a hit
            ship_sunk (bool): Whether a ship was sunk
            game_over (bool): Whether the game is over
        """
        pass

    def get_name(self):
        """Get the name of the AI strategy.

        Returns:
            str: The name of the AI strategy
        """
        return self.name

    def get_description(self):
        """Get the description of the AI strategy.

        Returns:
            str: The description of the AI strategy
        """
        return self.description
