from typing import Any
from player import Player


class Game:
    def __init__(self):
        self.players: dict[Any, Player] = {}
        self.keys: list = []
        self.turn = None

    def nextTurn(self):
        self.turn = self.keys.pop(0)
        self.keys.append(self.turn)
        return self.turn
