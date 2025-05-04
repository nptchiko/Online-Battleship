# Battleship Game Architecture

## Overview
This document outlines the architecture for a single-player Battleship game with bot opponents, following SOLID principles to ensure easy extension of AI models.

## SOLID Principles Application

### Single Responsibility Principle (SRP)
- Each class will have only one reason to change
- Separate concerns: game logic, UI, AI strategies

### Open/Closed Principle (OCP)
- Game components will be open for extension but closed for modification
- AI strategies can be added without modifying existing code

### Liskov Substitution Principle (LSP)
- AI strategy implementations will be substitutable for their base class/interface
- Different AI players can be used interchangeably

### Interface Segregation Principle (ISP)
- Specific interfaces for different components
- AI strategies will implement only the methods they need

### Dependency Inversion Principle (DIP)
- High-level modules will not depend on low-level modules
- Both will depend on abstractions

## Core Components

### Models
- `Board`: Represents the game board with grid and ships
- `Ship`: Represents a ship with size, position, and orientation
- `Cell`: Represents a single cell on the board with state (empty, ship, hit, miss)
- `GameState`: Manages the current state of the game

### Game Logic
- `GameController`: Coordinates game flow and interactions
- `GameRules`: Enforces standard Battleship rules

### AI Strategy Interface
- `AIStrategy`: Interface for all AI implementations
  - `get_move()`: Returns the next move for the AI
  - `notify_result()`: Updates AI with the result of its last move

### AI Implementations
- `RandomAI`: Fires at random cells (initial implementation)
- `HuntTargetAI`: Switches to targeting mode after a hit (initial implementation)
- Future extensions (to be implemented by user):
  - `ParityAI`: Uses parity filter based on ship sizes
  - `ProbabilityDensityAI`: Calculates and targets highest probability cells
  - `MCTSAI`: Uses Monte Carlo Tree Search for decision-making
  - `NeuralNetworkAI`: Uses learned patterns for decision-making

### UI Components
- `GameView`: Main Tkinter window
- `BoardView`: Visual representation of the game board
- `ControlPanel`: UI controls for game settings and AI selection

## Component Interactions
1. `GameController` initializes the game with selected `AIStrategy`
2. Player places ships on their board through `BoardView`
3. Game loop begins:
   - Player takes a turn through UI
   - `GameController` processes the move and updates `GameState`
   - AI takes a turn using selected `AIStrategy`
   - `GameController` processes AI move and updates `GameState`
   - `BoardView` updates to reflect new game state
4. Game continues until win condition is met

## Extension Points
- New AI strategies can be added by implementing the `AIStrategy` interface
- UI can be extended with new views or controls
- Game rules can be modified by extending the `GameRules` class

## Class Diagram (Simplified)
```
+----------------+     +----------------+     +----------------+
|  GameController|---->|    GameState   |---->|     Board      |
+----------------+     +----------------+     +----------------+
        |                                            |
        |                                            |
        v                                            v
+----------------+     +----------------+     +----------------+
|    GameView    |     |   AIStrategy   |     |      Ship      |
+----------------+     +----------------+     +----------------+
        |                      ^                      
        |                      |                      
        v                      |                      
+----------------+     +----------------+     +----------------+
|    BoardView   |     |    RandomAI    |     |  HuntTargetAI  |
+----------------+     +----------------+     +----------------+
```
