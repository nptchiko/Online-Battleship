import tkinter as tk
from tkinter import ttk, messagebox
from models.ship import Orientation

class BoardView(tk.Canvas):
    """Canvas widget for displaying a Battleship game board."""
    
    def __init__(self, parent, board_size=10, cell_size=30, **kwargs):
        """Initialize the board view.
        
        Args:
            parent: The parent widget
            board_size (int): The size of the board (both width and height)
            cell_size (int): The size of each cell in pixels
        """
        self.board_size = board_size
        self.cell_size = cell_size
        canvas_size = board_size * cell_size
        
        super().__init__(
            parent,
            width=canvas_size,
            height=canvas_size,
            bg="white",
            **kwargs
        )
        
        self.grid_color = "#CCCCCC"
        self.ship_color = "#555555"
        self.hit_color = "#FF0000"
        self.miss_color = "#0000FF"
        
        self._draw_grid()
        
        # Bind events
        self.bind("<Button-1>", self._on_click)
        self.bind("<Motion>", self._on_motion)
        
        # Callback functions
        self.click_callback = None
        self.hover_callback = None
        
        # Placement preview
        self.preview_ship = None
        self.preview_orientation = Orientation.HORIZONTAL
        self.preview_valid = False
    
    def _draw_grid(self):
        """Draw the grid lines on the canvas."""
        # Draw horizontal grid lines
        for i in range(self.board_size + 1):
            y = i * self.cell_size
            self.create_line(0, y, self.board_size * self.cell_size, y, fill=self.grid_color)
        
        # Draw vertical grid lines
        for i in range(self.board_size + 1):
            x = i * self.cell_size
            self.create_line(x, 0, x, self.board_size * self.cell_size, fill=self.grid_color)
        
        # Add row and column labels
        for i in range(self.board_size):
            # Row labels (numbers)
            self.create_text(
                self.cell_size / 4,
                i * self.cell_size + self.cell_size / 2,
                text=str(i),
                font=("Arial", 8),
                fill="black"
            )
            
            # Column labels (letters)
            self.create_text(
                i * self.cell_size + self.cell_size / 2,
                self.cell_size / 4,
                text=chr(65 + i),  # A, B, C, ...
                font=("Arial", 8),
                fill="black"
            )
    
    def update_view(self, board, show_ships=True):
        """Update the view to reflect the current state of the board.
        
        Args:
            board: The board model to display
            show_ships (bool): Whether to show ships that haven't been hit
        """
        self.delete("cell")  # Remove all cell markers
        
        for row in range(self.board_size):
            for col in range(self.board_size):
                cell = board.get_cell(row, col)
                if cell:
                    x1 = col * self.cell_size
                    y1 = row * self.cell_size
                    x2 = x1 + self.cell_size
                    y2 = y1 + self.cell_size
                    
                    if cell.state.name == "HIT":
                        # Draw hit marker
                        self.create_rectangle(x1, y1, x2, y2, fill=self.hit_color, tags="cell")
                        self.create_line(x1, y1, x2, y2, fill="black", width=2, tags="cell")
                        self.create_line(x1, y2, x2, y1, fill="black", width=2, tags="cell")
                    
                    elif cell.state.name == "MISS":
                        # Draw miss marker
                        self.create_oval(
                            x1 + self.cell_size * 0.25,
                            y1 + self.cell_size * 0.25,
                            x2 - self.cell_size * 0.25,
                            y2 - self.cell_size * 0.25,
                            fill=self.miss_color,
                            tags="cell"
                        )
                    
                    elif cell.state.name == "SHIP" and show_ships:
                        # Draw ship
                        self.create_rectangle(
                            x1 + 1, y1 + 1, x2 - 1, y2 - 1,
                            fill=self.ship_color,
                            outline="",
                            tags="cell"
                        )
    
    def show_placement_preview(self, row, col, ship_size, orientation, valid):
        """Show a preview of ship placement.
        
        Args:
            row (int): The row index
            col (int): The column index
            ship_size (int): The size of the ship
            orientation (Orientation): The orientation of the ship
            valid (bool): Whether the placement is valid
        """
        self.delete("preview")  # Remove previous preview
        
        if row is None or col is None:
            return
        
        color = "#AAFFAA" if valid else "#FFAAAA"  # Green if valid, red if invalid
        
        for i in range(ship_size):
            r, c = row, col
            if orientation == Orientation.HORIZONTAL:
                c += i
            else:  # VERTICAL
                r += i
            
            if 0 <= r < self.board_size and 0 <= c < self.board_size:
                x1 = c * self.cell_size
                y1 = r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                self.create_rectangle(
                    x1 + 1, y1 + 1, x2 - 1, y2 - 1,
                    fill=color,
                    outline="",
                    tags="preview"
                )
    
    def clear_placement_preview(self):
        """Clear the ship placement preview."""
        self.delete("preview")
    
    def _on_click(self, event):
        """Handle mouse click events.
        
        Args:
            event: The click event
        """
        # Convert pixel coordinates to grid coordinates
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        
        if 0 <= row < self.board_size and 0 <= col < self.board_size:
            if self.click_callback:
                self.click_callback(row, col)
    
    def _on_motion(self, event):
        """Handle mouse motion events.
        
        Args:
            event: The motion event
        """
        # Convert pixel coordinates to grid coordinates
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        
        if 0 <= row < self.board_size and 0 <= col < self.board_size:
            if self.hover_callback:
                self.hover_callback(row, col)
    
    def set_click_callback(self, callback):
        """Set the callback function for click events.
        
        Args:
            callback: The callback function
        """
        self.click_callback = callback
    
    def set_hover_callback(self, callback):
        """Set the callback function for hover events.
        
        Args:
            callback: The callback function
        """
        self.hover_callback = callback
