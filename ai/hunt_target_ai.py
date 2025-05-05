from ai.ai_strategy import AIStrategy
import random


class HuntTargetAI(AIStrategy):
    """AI strategy that switches to targeting mode after a hit."""

    def __init__(self, board_size=10):
        """Initialize the Hunt & Target AI strategy.

        Args:
            board_size (int): The size of the game board
        """
        super().__init__(board_size)
        self.name = "Hunt & Target AI"
        self.description = "Switches to targeting mode after a hit. Medium efficiency, easy to implement."
        self.available_moves = [(r, c) for r in range(board_size)
                                for c in range(board_size)]
        random.shuffle(self.available_moves)
        self.mode = "hunt"  # "hunt" or "target"
        self.last_hit = None
        self.hits = []  # List of successful hits that are part of the current ship
        self.targets = []  # Potential targets around hits

    def get_move(self, opponent_board):
        """Get the next move for the AI.

        Args:
            opponent_board: The opponent's board

        Returns:
            tuple: (row, col) coordinates for the next shot
        """
        if self.mode == "target" and self.targets:
            # Target mode: choose from the target list
            move = self.targets.pop(0)
            # Ensure the move is valid (not already taken)
            while move not in self.available_moves and self.targets:
                move = self.targets.pop(0)

            if move in self.available_moves:
                self.available_moves.remove(move)
                return move

        # Hunt mode or no valid targets: choose a random move
        self.mode = "hunt"
        if not self.available_moves:
            return None

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
        if hit:
            self.mode = "target"
            self.last_hit = (row, col)
            self.hits.append((row, col))

            # Add adjacent cells to the target list if not already targeted
            self._add_adjacent_targets(row, col)

            # If we have multiple hits, try to align targets along the ship axis
            if len(self.hits) >= 2:
                self._align_targets()

        if ship_sunk:
            # Reset targeting when a ship is sunk
            self.mode = "hunt"
            self.hits = []
            self.targets = []

    def _add_adjacent_targets(self, row, col):
        """Add adjacent cells to the target list.

        Args:
            row (int): The row index of the hit
            col (int): The column index of the hit
        """
        # Check all four directions (up, right, down, left)
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

        for dr, dc in directions:
            r, c = row + dr, col + dc
            if (0 <= r < self.board_size and 0 <= c < self.board_size and
                    (r, c) in self.available_moves and (r, c) not in self.targets):
                self.targets.append((r, c))

    def _align_targets(self):
        """Align targets along the ship axis if multiple hits are found."""
        if len(self.hits) < 2:
            return

        # Clear current targets
        self.targets = []

        # Determine if the ship is horizontal or vertical
        horizontal = all(hit[0] == self.hits[0][0] for hit in self.hits)
        vertical = all(hit[1] == self.hits[0][1] for hit in self.hits)

        if horizontal:
            # Ship is horizontal, add targets to the left and right
            min_col = min(hit[1] for hit in self.hits)
            max_col = max(hit[1] for hit in self.hits)
            row = self.hits[0][0]

            # Add target to the left
            if min_col > 0 and (row, min_col - 1) in self.available_moves:
                self.targets.append((row, min_col - 1))

            # Add target to the right
            if max_col < self.board_size - 1 and (row, max_col + 1) in self.available_moves:
                self.targets.append((row, max_col + 1))

        elif vertical:
            # Ship is vertical, add targets above and below
            min_row = min(hit[0] for hit in self.hits)
            max_row = max(hit[0] for hit in self.hits)
            col = self.hits[0][1]

            # Add target above
            if min_row > 0 and (min_row - 1, col) in self.available_moves:
                self.targets.append((min_row - 1, col))

            # Add target below
            if max_row < self.board_size - 1 and (max_row + 1, col) in self.available_moves:
                self.targets.append((max_row + 1, col))

        # If no aligned targets found, fall back to adjacent targets
        if not self.targets and self.last_hit:
            self._add_adjacent_targets(self.last_hit[0], self.last_hit[1])
