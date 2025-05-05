import tkinter as tk
from tkinter import ttk, messagebox
from models.ship import Orientation
from models.game_state import GamePhase
from ai.random_ai import RandomAI
from ai.hunt_target_ai import HuntTargetAI
from ai.Probalisty_AI  import OptimizedProbabilityAI

class ControlPanel(tk.Frame):
    """Control panel for the Battleship game."""
    
    def __init__(self, parent, **kwargs):
        """Initialize the control panel.
        
        Args:
            parent: The parent widget
        """
        super().__init__(parent, **kwargs)
        
        self.ai_strategies = {
            "Random AI": RandomAI,
            "Hunt & Target AI": HuntTargetAI,
            "Probalisty AI ":OptimizedProbabilityAI
        }
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create the control panel widgets."""
        # Game status label
        self.status_label = ttk.Label(self, text="Welcome to Battleship!", font=("Arial", 12))
        self.status_label.pack(pady=10)
        
        # Ship placement frame
        self.placement_frame = ttk.LabelFrame(self, text="Ship Placement")
        self.placement_frame.pack(fill="x", padx=10, pady=5)
        
        # Orientation selection
        self.orientation_var = tk.StringVar(value="Horizontal")
        ttk.Label(self.placement_frame, text="Orientation:").pack(side="left", padx=5)
        self.orientation_menu = ttk.OptionMenu(
            self.placement_frame,
            self.orientation_var,
            "Horizontal",
            "Horizontal",
            "Vertical",
            command=self._on_orientation_change
        )
        self.orientation_menu.pack(side="left", padx=5)
        
        # Random placement button
        self.random_placement_button = ttk.Button(
            self.placement_frame,
            text="Random Placement",
            command=self._on_random_placement
        )
        self.random_placement_button.pack(side="right", padx=5)
        
        # AI selection frame
        self.ai_frame = ttk.LabelFrame(self, text="AI Opponent")
        self.ai_frame.pack(fill="x", padx=10, pady=5)
        
        # AI strategy selection
        self.ai_var = tk.StringVar(value="Random AI")
        ttk.Label(self.ai_frame, text="AI Strategy:").pack(side="left", padx=5)
        self.ai_menu = ttk.OptionMenu(
            self.ai_frame,
            self.ai_var,
            "Random AI",
            *self.ai_strategies.keys(),
            command=self._on_ai_change
        )
        self.ai_menu.pack(side="left", padx=5)
        
        # AI description label
        self.ai_description = ttk.Label(
            self.ai_frame,
            text="Fires at random cells. Low efficiency, easy to implement.",
            wraplength=250
        )
        self.ai_description.pack(side="left", padx=5, fill="x", expand=True)
        
        # Game control frame
        self.game_control_frame = ttk.Frame(self)
        self.game_control_frame.pack(fill="x", padx=10, pady=10)
        
        # New game button
        self.new_game_button = ttk.Button(
            self.game_control_frame,
            text="New Game",
            command=self._on_new_game
        )
        self.new_game_button.pack(side="left", padx=5)
        
        # Quit button
        self.quit_button = ttk.Button(
            self.game_control_frame,
            text="Quit",
            command=self._on_quit
        )
        self.quit_button.pack(side="right", padx=5)
        
        # Callback functions
        self.new_game_callback = None
        self.random_placement_callback = None
        self.orientation_change_callback = None
        self.ai_change_callback = None
        self.quit_callback = None
    
    def update_status(self, message):
        """Update the status message.
        
        Args:
            message (str): The new status message
        """
        self.status_label.config(text=message)
    
    def update_game_phase(self, phase):
        """Update the UI based on the current game phase.
        
        Args:
            phase (GamePhase): The current game phase
        """
        if phase == GamePhase.SETUP:
            self.placement_frame.pack(fill="x", padx=10, pady=5)
            self.orientation_menu.config(state="normal")
            self.random_placement_button.config(state="normal")
        else:
            self.placement_frame.pack_forget()
    
    def get_orientation(self):
        """Get the selected ship orientation.
        
        Returns:
            Orientation: The selected orientation
        """
        return Orientation.HORIZONTAL if self.orientation_var.get() == "Horizontal" else Orientation.VERTICAL
    
    def get_ai_strategy(self):
        """Get the selected AI strategy class.
        
        Returns:
            class: The selected AI strategy class
        """
        return self.ai_strategies[self.ai_var.get()]
    
    def _on_orientation_change(self, *args):
        """Handle orientation change events."""
        if self.orientation_change_callback:
            orientation = self.get_orientation()
            self.orientation_change_callback(orientation)
    
    def _on_random_placement(self):
        """Handle random placement button click events."""
        if self.random_placement_callback:
            self.random_placement_callback()
    
    def _on_new_game(self):
        """Handle new game button click events."""
        if self.new_game_callback:
            self.new_game_callback()
    
    def _on_ai_change(self, *args):
        """Handle AI strategy change events."""
        # Update AI description
        ai_class = self.ai_strategies[self.ai_var.get()]
        ai_instance = ai_class()
        self.ai_description.config(text=ai_instance.get_description())
        
        if self.ai_change_callback:
            self.ai_change_callback(ai_class)
    
    def _on_quit(self):
        """Handle quit button click events."""
        if self.quit_callback:
            self.quit_callback()
    
    def set_new_game_callback(self, callback):
        """Set the callback function for new game events.
        
        Args:
            callback: The callback function
        """
        self.new_game_callback = callback
    
    def set_random_placement_callback(self, callback):
        """Set the callback function for random placement events.
        
        Args:
            callback: The callback function
        """
        self.random_placement_callback = callback
    
    def set_orientation_change_callback(self, callback):
        """Set the callback function for orientation change events.
        
        Args:
            callback: The callback function
        """
        self.orientation_change_callback = callback
    
    def set_ai_change_callback(self, callback):
        """Set the callback function for AI strategy change events.
        
        Args:
            callback: The callback function
        """
        self.ai_change_callback = callback
    
    def set_quit_callback(self, callback):
        """Set the callback function for quit events.
        
        Args:
            callback: The callback function
        """
        self.quit_callback = callback
