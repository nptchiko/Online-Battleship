from ai.ai_strategy import AIStrategy
import random


class RandomAI(AIStrategy):

    def __init__(self, board_size=10):
        super().__init__(board_size)
        self.name = "Random AI"
        self.description = "Fires at random cells. Low efficiency, easy to implement."
        self.available_moves = [(r, c) for r in range(board_size)
                                for c in range(board_size)]
        random.shuffle(self.available_moves)

    def get_move(self, opponent_board):
        # If no more available moves, return None
        if not self.available_moves:
            return None

        # Get the next random move
        return self.available_moves.pop()

    def notify_result(self, row, col, hit, ship_sunk, game_over):
        # Random AI doesn't need to track results
        pass
