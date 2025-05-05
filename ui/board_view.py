import tkinter as tk
from tkinter import ttk
from models.ship import Orientation

class BoardView(tk.Canvas):
    """Canvas widget for displaying a Battleship game board."""
    
    def __init__(self, parent, board_size=10, cell_size=35, **kwargs):
        """Initialize the board view.
        
        Args:
            parent: The parent widget
            board_size (int): The size of the board (both width and height)
            cell_size (int): The size of each cell in pixels
        """
        self.board_size = board_size
        self.cell_size = cell_size
        
        # Add margin for labels
        self.margin = 25
        canvas_size = board_size * cell_size + self.margin
        
        super().__init__(
            parent,
            width=canvas_size,
            height=canvas_size,
            bg="#E6F2FF",  # Light blue background for water
            highlightthickness=1,
            highlightbackground="#003366",
            **kwargs
        )
        
        # Improved colors
        self.grid_color = "#7AA5D2"  # Softer blue for grid
        self.ship_color = "#3D5A80"  # Navy blue for ships
        self.hit_color = "#E63946"   # Bright red for hits
        self.miss_color = "#A8DADC"  # Light blue for misses
        self.preview_valid_color = "#90EE90"  # Light green for valid placement
        self.preview_invalid_color = "#FFA07A"  # Light salmon for invalid placement
        
        self._draw_grid()
        
        # Bind events
        self.bind("<Button-1>", self._on_click)
        self.bind("<Motion>", self._on_motion)
        self.bind("<Leave>", self._on_leave)
        
        # Callback functions
        self.click_callback = None
        self.hover_callback = None
        
        # Placement preview
        self.preview_cells = []
        self.preview_valid = False
    
    def _draw_grid(self):
        """Draw the grid lines and labels on the canvas."""
        # Draw horizontal grid lines
        for i in range(self.board_size + 1):
            y = i * self.cell_size + self.margin
            self.create_line(
                self.margin, y, 
                self.board_size * self.cell_size + self.margin, y, 
                fill=self.grid_color, width=1
            )
        
        # Draw vertical grid lines
        for i in range(self.board_size + 1):
            x = i * self.cell_size + self.margin
            self.create_line(
                x, self.margin, 
                x, self.board_size * self.cell_size + self.margin, 
                fill=self.grid_color, width=1
            )
        
        # Add row and column labels with improved styling (outside the grid)
        for i in range(self.board_size):
            # Row labels (numbers) - now on the left side of the grid
            self.create_text(
                self.margin / 2,
                i * self.cell_size + self.margin + self.cell_size / 2,
                text=str(i),
                font=("Arial", 9, "bold"),
                fill="#003366"
            )
            
            # Column labels (letters) - now above the grid
            self.create_text(
                i * self.cell_size + self.margin + self.cell_size / 2,
                self.margin / 2,
                text=chr(65 + i),  # A, B, C, ...
                font=("Arial", 9, "bold"),
                fill="#003366"
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
                    x1 = col * self.cell_size + self.margin + 2
                    y1 = row * self.cell_size + self.margin + 2
                    x2 = x1 + self.cell_size - 4
                    y2 = y1 + self.cell_size - 4
                    
                    if cell.state.name == "HIT":
                        # Draw hit marker with improved styling
                        self.create_rectangle(x1, y1, x2, y2, fill=self.hit_color, outline="", tags="cell")
                        self.create_line(x1+2, y1+2, x2-2, y2-2, fill="white", width=2, tags="cell")
                        self.create_line(x1+2, y2-2, x2-2, y1+2, fill="white", width=2, tags="cell")
                    
                    elif cell.state.name == "MISS":
                        # Draw miss marker with improved styling
                        self.create_oval(
                            x1 + self.cell_size * 0.25,
                            y1 + self.cell_size * 0.25,
                            x2 - self.cell_size * 0.25,
                            y2 - self.cell_size * 0.25,
                            fill=self.miss_color,
                            outline="#5D8AA8",
                            width=1,
                            tags="cell"
                        )
                    
                    elif cell.state.name == "SHIP" and show_ships:
                        # Draw ship with improved styling
                        self.create_rounded_rectangle(
                            x1, y1, x2, y2,
                            radius=5,
                            fill=self.ship_color,
                            outline="#1A3A5A",
                            width=1,
                            tags="cell"
                        )
    
    def create_rounded_rectangle(self, x1, y1, x2, y2, radius=10, **kwargs):
        """Create a rounded rectangle on the canvas.
        
        Args:
            x1, y1: Top-left corner coordinates
            x2, y2: Bottom-right corner coordinates
            radius: Corner radius
            **kwargs: Additional arguments for create_polygon
        """
        points = [
            x1+radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)
    
    def show_placement_preview(self, ship_coords, valid):
        """Show a preview of ship placement.
        
        Args:
            ship_coords (list): List of (row, col) tuples for ship cells
            valid (bool): Whether the placement is valid
        """
        self.delete("preview")  # Remove previous preview
        
        if not ship_coords:
            return
        
        color = self.preview_valid_color if valid else self.preview_invalid_color
        
        for r, c in ship_coords:
            x1 = c * self.cell_size + self.margin + 2
            y1 = r * self.cell_size + self.margin + 2
            x2 = x1 + self.cell_size - 4
            y2 = y1 + self.cell_size - 4
            
            self.create_rounded_rectangle(
                x1, y1, x2, y2,
                radius=5,
                fill=color,
                outline="#555555" if valid else "#AA3333",
                width=1,
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
        # Convert pixel coordinates to grid coordinates, accounting for margin
        col = (event.x - self.margin) // self.cell_size
        row = (event.y - self.margin) // self.cell_size
        
        if 0 <= row < self.board_size and 0 <= col < self.board_size:
            if self.click_callback:
                self.click_callback(row, col)
    
    def _on_motion(self, event):
        """Handle mouse motion events.
        
        Args:
            event: The motion event
        """
        # Convert pixel coordinates to grid coordinates, accounting for margin
        col = (event.x - self.margin) // self.cell_size
        row = (event.y - self.margin) // self.cell_size
        
        if 0 <= row < self.board_size and 0 <= col < self.board_size:
            if self.hover_callback:
                self.hover_callback(row, col)
    
    def _on_leave(self, event):
        """Handle mouse leave events.
        
        Args:
            event: The leave event
        """
        # Clear the preview when mouse leaves the canvas
        self.clear_placement_preview()
    
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