# Battleship Game - README

## Overview

This is a single-player Battleship game with bot opponents, implemented in Python using Tkinter as the UI library. The game follows standard Battleship rules and includes two AI strategies (Random and Hunt & Target), with an architecture designed to make it easy to extend with more complex AI models in the future.

## Features

- Standard Battleship rules (10x10 grid, 5 ships of different sizes)
- Two AI strategies:
  - Random AI: Fires at random cells (low efficiency, easy to implement)
  - Hunt & Target AI: Switches to targeting mode after a hit (medium efficiency, easy to implement)
- Clean, intuitive Tkinter UI
- Architecture designed for easy extension with more complex AI models

## Requirements

- Python 3.6 or higher
- Tkinter (usually comes with Python installation)

## How to Run the Game

1. Navigate to the game directory
2. Run the main.py file:

```
python3 main.py
```

## Game Instructions

1. When the game starts, you'll need to place your ships on your board
2. You can change the orientation of ships using the dropdown menu
3. Click on your board to place ships, or use the "Random Placement" button
4. Once all ships are placed, you can start firing at the opponent's board
5. Click on the opponent's board to fire
6. The game ends when either all your ships or all the opponent's ships are sunk

## Project Structure

- `models/`: Core game models (Board, Ship, Cell, GameState)
- `ai/`: AI strategy implementations
- `ui/`: Tkinter UI components
- `main.py`: Main entry point for the game

### Example of a New AI Strategy

```python
from ai.ai_strategy import AIStrategy
import random

class ParityAI(AIStrategy):
    """AI strategy that uses a parity filter based on ship sizes."""

    def __init__(self, board_size=10):
        """Initialize the Parity AI strategy."""
        super().__init__(board_size)
        self.name = "Parity AI"
        self.description = "Hunts using a parity filter based on ship sizes. High efficiency, medium complexity."
        self.available_moves = []
        self.hits = []
        self.targets = []
        self.init_parity_grid()

    def init_parity_grid(self):
        """Initialize the parity grid based on ship sizes."""
        # Implementation details here
        pass

    def get_move(self, opponent_board):
        """Get the next move for the AI."""
        # Implementation details here
        pass

    def notify_result(self, row, col, hit, ship_sunk, game_over):
        """Update the AI with the result of its last move."""
        # Implementation details here
        pass
```

## License

This project is open source and available for personal and educational use.
