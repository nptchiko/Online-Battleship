from board import Board


class Player:
    def __init__(self):
        self.board = Board()
        self.placedShip: bool = False

    def isHit(self, coord: tuple):
        for ship in self.board.shipList:
            if coord in ship.coordList:
                return True
        return False

    def shoot(self, player, coord: tuple):
        result: bool = player.isHit(coord)

        if result:
            self.board.hitList.append(coord)
        else:
            self.board.missedList.append(coord)
        return {"coord": coord, "result": result}
