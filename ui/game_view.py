import tkinter as tk
from tkinter import ttk, messagebox
from models.game_state import GameState, GamePhase
from models.ship import Orientation
from ui.board_view import BoardView
from ui.control_panel import ControlPanel

class GameView(tk.Tk):
    """Main window for the Battleship game."""
    
    def __init__(self):
        """Initialize the game view."""
        super().__init__()
        
        self.title("Battleship Game")
        self.resizable(False, False)
        
        self.game_state = None
        self.ai_strategy = None
        
        self._create_widgets()
        self._setup_callbacks()
        
        # Start a new game
        self._new_game()
    
    def _create_widgets(self):
        """Create the game view widgets."""
        # Main frame
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill="both", expand=True)
        
        # Boards frame
        boards_frame = ttk.Frame(main_frame)
        boards_frame.pack(fill="both", expand=True)
        
        # Player board frame
        player_frame = ttk.LabelFrame(boards_frame, text="Your Board")
        player_frame.pack(side="left", padx=10, pady=10)
        
        # Player board view
        self.player_board_view = BoardView(player_frame)
        self.player_board_view.pack(padx=5, pady=5)
        
        # AI board frame
        ai_frame = ttk.LabelFrame(boards_frame, text="Opponent's Board")
        ai_frame.pack(side="right", padx=10, pady=10)
        
        # AI board view
        self.ai_board_view = BoardView(ai_frame)
        self.ai_board_view.pack(padx=5, pady=5)
        
        # Control panel
        self.control_panel = ControlPanel(main_frame)
        self.control_panel.pack(fill="x", padx=10, pady=10)
    
    def _setup_callbacks(self):
        """Set up callback functions."""
        # Player board callbacks
        self.player_board_view.set_click_callback(self._on_player_board_click)
        self.player_board_view.set_hover_callback(self._on_player_board_hover)
        
        # AI board callbacks
        self.ai_board_view.set_click_callback(self._on_ai_board_click)
        
        # Control panel callbacks
        self.control_panel.set_new_game_callback(self._new_game)
        self.control_panel.set_random_placement_callback(self._random_placement)
        self.control_panel.set_orientation_change_callback(self._on_orientation_change)
        self.control_panel.set_ai_change_callback(self._on_ai_change)
        self.control_panel.set_quit_callback(self._quit)
    
    def _new_game(self):
        """Start a new game."""
        # Create a new game state
        self.game_state = GameState()
        
        # Create a new AI strategy
        ai_class = self.control_panel.get_ai_strategy()
        self.ai_strategy = ai_class()
        
        # Set up the game
        self.game_state.setup_game()
        
        # Update the UI
        self._update_ui()
    
    def _update_ui(self):
        """Update the UI to reflect the current game state."""
        # Update board views
        self.player_board_view.update_view(self.game_state.get_player_board(), show_ships=True)
        self.ai_board_view.update_view(self.game_state.get_ai_board(), show_ships=False)
        
        # Update control panel
        self.control_panel.update_status(self.game_state.get_message())
        self.control_panel.update_game_phase(self.game_state.get_current_phase())
        
        # Update ship placement preview
        if self.game_state.get_current_phase() == GamePhase.SETUP:
            current_ship = self.game_state.get_current_ship()
            if current_ship:
                self.current_ship_size = current_ship[0]
            else:
                self.current_ship_size = None
        else:
            self.current_ship_size = None
            self.player_board_view.clear_placement_preview()
    
    def _on_player_board_click(self, row, col):
        """Handle clicks on the player's board.
        
        Args:
            row (int): The row index
            col (int): The column index
        """
        if self.game_state.get_current_phase() == GamePhase.SETUP:
            # Place a ship
            orientation = self.control_panel.get_orientation()
            success = self.game_state.place_player_ship(row, col, orientation)
            
            # Update the UI
            self._update_ui()
            
            # Check if all ships are placed
            if self.game_state.get_current_phase() == GamePhase.PLAYER_TURN:
                messagebox.showinfo("Ships Placed", "All ships placed. Your turn to fire!")
    
    def _on_player_board_hover(self, row, col):
        """Handle hover events on the player's board.
        
        Args:
            row (int): The row index
            col (int): The column index
        """
        if self.game_state.get_current_phase() == GamePhase.SETUP and self.current_ship_size:
            # Show ship placement preview
            orientation = self.control_panel.get_orientation()
            
            # Check if placement is valid
            valid = self._can_place_ship(row, col, self.current_ship_size, orientation)
            
            # Show preview
            self.player_board_view.show_placement_preview(
                row, col, self.current_ship_size, orientation, valid
            )
    
    def _can_place_ship(self, row, col, ship_size, orientation):
        """Check if a ship can be placed at the specified position.
        
        Args:
            row (int): The row index
            col (int): The column index
            ship_size (int): The size of the ship
            orientation (Orientation): The orientation of the ship
        
        Returns:
            bool: True if the ship can be placed, False otherwise
        """
        board = self.game_state.get_player_board()
        
        # Check if the ship would go out of bounds
        if orientation == Orientation.HORIZONTAL:
            if col + ship_size > board.size:
                return False
        else:  # VERTICAL
            if row + ship_size > board.size:
                return False
        
        # Check if the ship would overlap with another ship
        for i in range(ship_size):
            r, c = row, col
            if orientation == Orientation.HORIZONTAL:
                c += i
            else:  # VERTICAL
                r += i
            
            # Check if the cell already has a ship
            if board.get_cell(r, c).has_ship():
                return False
            
            # Check adjacent cells (optional, for spacing between ships)
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = r + dr, c + dc
                    if (0 <= nr < board.size and 0 <= nc < board.size and 
                        (nr != r or nc != c)):
                        cell = board.get_cell(nr, nc)
                        if cell and cell.has_ship():
                            return False
        
        return True
    
    def _on_ai_board_click(self, row, col):
        """Handle clicks on the AI's board.
        
        Args:
            row (int): The row index
            col (int): The column index
        """
        if self.game_state.get_current_phase() == GamePhase.PLAYER_TURN:
            # Player's turn to fire
            valid_move, hit, ship_sunk, game_over = self.game_state.player_shoot(row, col)
            
            if valid_move:
                # Update the UI
                self._update_ui()
                
                if game_over:
                    messagebox.showinfo("Game Over", "Congratulations! You won the game!")
                    return
                
                # AI's turn
                self._ai_turn()
    
    def _ai_turn(self):
        """Handle the AI's turn."""
        if self.game_state.get_current_phase() == GamePhase.AI_TURN:
            # Get the AI's move
            row, col = self.ai_strategy.get_move(self.game_state.get_player_board())
            
            if row is not None and col is not None:
                # AI fires
                hit, ship_sunk, game_over = self.game_state.ai_shoot(row, col)
                
                # Notify the AI of the result
                self.ai_strategy.notify_result(row, col, hit, ship_sunk, game_over)
                
                # Update the UI
                self._update_ui()
                
                if game_over:
                    messagebox.showinfo("Game Over", "Game over! The AI won.")
    
    def _random_placement(self):
        """Place ships randomly."""
        success = self.game_state.place_player_ships_randomly()
        
        if success:
            # Update the UI
            self._update_ui()
            
            # Check if all ships are placed
            if self.game_state.get_current_phase() == GamePhase.PLAYER_TURN:
                messagebox.showinfo("Ships Placed", "All ships placed randomly. Your turn to fire!")
        else:
            messagebox.showerror("Error", "Failed to place ships randomly. Please try again.")
    
    def _on_orientation_change(self, orientation):
        """Handle orientation change events.
        
        Args:
            orientation (Orientation): The new orientation
        """
        # Update the preview if hovering over the player's board
        if hasattr(self, 'last_hover_pos'):
            row, col = self.last_hover_pos
            self._on_player_board_hover(row, col)
    
    def _on_ai_change(self, ai_class):
        """Handle AI strategy change events.
        
        Args:
            ai_class: The new AI strategy class
        """
        # Create a new AI strategy
        self.ai_strategy = ai_class()
    
    def _quit(self):
        """Quit the game."""
        if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
            self.destroy()

def run_game():
    """Run the Battleship game."""
    game = GameView()
    game.mainloop()
