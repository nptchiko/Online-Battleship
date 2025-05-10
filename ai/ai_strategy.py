from abc import ABC, abstractmethod
import random
from models.cell import CellState


class AIStrategy(ABC):

    def __init__(self, board_size=10):
        self.board_size = board_size
        self.name = "Base AI"
        self.description = "Base AI strategy"

    @abstractmethod
    def get_move(self, opponent_board):
        pass

    @abstractmethod
    def notify_result(self, row, col, hit, ship_sunk, game_over):
        pass

    def get_name(self):

        return self.name

    def get_description(self):
        return self.description
