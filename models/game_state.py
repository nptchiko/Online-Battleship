from enum import Enum
from models.board import Board
from models.ship import Ship, Orientation


class GamePhase(Enum):
    """Enum representing the possible phases of the game."""
    SETUP = 0
    PLAYER_TURN = 1
    AI_TURN = 2
    GAME_OVER = 3


class GameState:
    """Manages the current state of the Battleship game."""

    # Standard ship configurations for Battleship
    STANDARD_SHIPS = [
        (5, "Carrier"),
        (4, "Battleship"),
        (3, "Cruiser"),
        (3, "Submarine"),
        (2, "Destroyer")
    ]

    def __init__(self, board_size=10):
        """Initialize the game state.

        Args:
            board_size (int): The size of the game boards
        """
        self.player_board = Board(board_size)
        self.ai_board = Board(board_size)
        self.phase = GamePhase.SETUP
        self.winner = None
        self.last_shot = None
        self.last_result = (False, False, False)  # (hit, sunk, game_over)
        self.ships_to_place = list(self.STANDARD_SHIPS)
        self.current_ship_index = 0
        self.message = "Welcome to Battleship! Place your ships."

    def setup_game(self, ai_place_randomly=True):
        """Set up the game boards.

        Args:
            ai_place_randomly (bool): Whether to place AI ships randomly

        Returns:
            bool: True if setup was successful, False otherwise
        """
        # Reset boards
        self.player_board.reset()
        self.ai_board.reset()

        # Place AI ships randomly
        if ai_place_randomly:
            success = self.ai_board.place_ships_randomly(self.STANDARD_SHIPS)
            if not success:
                self.message = "Failed to place AI ships. Please try again."
                return False

        self.phase = GamePhase.SETUP
        self.winner = None
        self.last_shot = None
        self.last_result = (False, False, False)
        self.ships_to_place = list(self.STANDARD_SHIPS)
        self.current_ship_index = 0
        self.message = "Place your ships on the board."

        return True

    def place_player_ship(self, row, col, orientation):
        """Place a player ship on the board.

        Args:
            row (int): The starting row index
            col (int): The starting column index
            orientation (Orientation): The orientation of the ship

        Returns:
            bool: True if the ship was placed successfully, False otherwise
        """
        if self.phase != GamePhase.SETUP or self.current_ship_index >= len(self.ships_to_place):
            return False

        size, name = self.ships_to_place[self.current_ship_index]
        ship = Ship(size, name)

        success = self.player_board.place_ship(ship, row, col, orientation)
        if success:
            self.current_ship_index += 1

            if self.current_ship_index >= len(self.ships_to_place):
                self.phase = GamePhase.PLAYER_TURN
                self.message = "All ships placed. Your turn to fire!"
            else:
                next_size, next_name = self.ships_to_place[self.current_ship_index]
                self.message = f"Place your {next_name} ({next_size} cells)"
        else:
            self.message = f"Cannot place {name} at that position. Try again."

        return success

    def place_player_ships_randomly(self):
        """Place player ships randomly on the board.

        Returns:
            bool: True if all ships were placed successfully, False otherwise
        """
        success = self.player_board.place_ships_randomly(self.STANDARD_SHIPS)
        if success:
            self.current_ship_index = len(self.ships_to_place)
            self.phase = GamePhase.PLAYER_TURN
            self.message = "Ships placed randomly. Your turn to fire!"
        else:
            self.message = "Failed to place ships randomly. Please try again."

        return success

    def player_shoot(self, row, col):
        """Process a shot fired by the player.

        Args:
            row (int): The row index of the target cell
            col (int): The column index of the target cell

        Returns:
            tuple: (valid_move, hit, ship_sunk, game_over)
        """
        if self.phase != GamePhase.PLAYER_TURN:
            return False, False, False, False

        hit, ship_sunk, game_over = self.ai_board.receive_shot(row, col)
        self.last_shot = (row, col)
        self.last_result = (hit, ship_sunk, game_over)

        if game_over:
            self.phase = GamePhase.GAME_OVER
            self.winner = "Player"
            self.message = "Congratulations! You won the game!"
        else:
            self.phase = GamePhase.AI_TURN
            if hit:
                if ship_sunk:
                    self.message = "Hit and sunk! AI's turn."
                else:
                    self.message = "Hit! AI's turn."
            else:
                self.message = "Miss! AI's turn."

        return True, hit, ship_sunk, game_over

    def ai_shoot(self, row, col):
        """Process a shot fired by the AI.

        Args:
            row (int): The row index of the target cell
            col (int): The column index of the target cell

        Returns:
            tuple: (hit, ship_sunk, game_over)
        """
        if self.phase != GamePhase.AI_TURN:
            return False, False, False

        hit, ship_sunk, game_over = self.player_board.receive_shot(row, col)
        self.last_shot = (row, col)
        self.last_result = (hit, ship_sunk, game_over)

        if game_over:
            self.phase = GamePhase.GAME_OVER
            self.winner = "AI"
            self.message = "Game over! The AI won."
        else:
            self.phase = GamePhase.PLAYER_TURN
            if hit:
                if ship_sunk:
                   self.message = f"AI hit and sunk your ship at ({row}, {col})! Your turn."

                else:
                     self.message = f"AI hit your ship at ({row}, {col})! Your turn."
            else:
                self.message = f"AI missed at ({row}, {col})! Your turn."

        return hit, ship_sunk, game_over

    def is_game_over(self):
        """Check if the game is over.

        Returns:
            bool: True if the game is over, False otherwise
        """
        return self.phase == GamePhase.GAME_OVER

    def get_current_phase(self):
        """Get the current game phase.

        Returns:
            GamePhase: The current game phase
        """
        return self.phase

    def get_message(self):
        """Get the current game message.

        Returns:
            str: The current game message
        """
        return self.message

    def get_winner(self):
        """Get the winner of the game.

        Returns:
            str: The winner of the game, or None if the game is not over
        """
        return self.winner

    def get_player_board(self):
        """Get the player's board.

        Returns:
            Board: The player's board
        """
        return self.player_board

    def get_ai_board(self):
        """Get the AI's board.

        Returns:
            Board: The AI's board
        """
        return self.ai_board

    def get_current_ship(self):
        """Get the current ship to place.

        Returns:
            tuple: (size, name) of the current ship to place, or None if all ships are placed
        """
        if self.phase == GamePhase.SETUP and self.current_ship_index < len(self.ships_to_place):
            return self.ships_to_place[self.current_ship_index]
        return None
