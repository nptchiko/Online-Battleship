from player import Player
from user import User


class PlayerUser(Player):
    def __init__(self, user: User):
        super().__init__()
        self.user = user

    def __str__(self):
        return "{}".format(self.user.name)
