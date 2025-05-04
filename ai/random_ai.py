from ai.ai_strategy import AIStrategy
import random

class RandomAI(AIStrategy):
    """AI strategy that fires at random cells."""
    
    def __init__(self, board_size=10):
        """Initialize the Random AI strategy.
        
        Args:
            board_size (int): The size of the game board
        """
        super().__init__(board_size)
        self.name = "Random AI"
        self.description = "Fires at random cells. Low efficiency, easy to implement."
        self.available_moves = [(r, c) for r in range(board_size) for c in range(board_size)]
        random.shuffle(self.available_moves)
    
    def get_move(self, opponent_board):
        """Get the next move for the AI.
        
        Args:
            opponent_board: The opponent's board
            
        Returns:
            tuple: (row, col) coordinates for the next shot
        """
        # If no more available moves, return None
        if not self.available_moves:
            return None
        
        # Get the next random move
        return self.available_moves.pop()
    
    def notify_result(self, row, col, hit, ship_sunk, game_over):
        """Update the AI with the result of its last move.
        
        Args:
            row (int): The row index of the last shot
            col (int): The column index of the last shot
            hit (bool): Whether the shot was a hit
            ship_sunk (bool): Whether a ship was sunk
            game_over (bool): Whether the game is over
        """
        # Random AI doesn't need to track results
        pass
