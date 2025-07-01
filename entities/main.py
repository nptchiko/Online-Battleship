# Example usage and testing
from direction import Direction
from ship import Ship
from ai_player import AIPlayer

# Example usage
if __name__ == "__main__":
    # Create a ship
    ship = Ship(4, 4, 3, Direction.NORTH)
    
    # Create an AI player
    player = AIPlayer()
    
    # Add ships to the board
    player.board.addShip(ship)
    player.board.addShip(Ship(5, 5, 5, Direction.NORTH))
    player.board.addShip(Ship(2, 7, 5, Direction.EAST))
    
    # Print the board
    player.board.printBoard()
