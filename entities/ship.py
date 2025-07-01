from direction import Direction


class Ship:
    def __init__(self, x, y, len, d: Direction):
        self.coord = (x, y)
        self.len = len
        self.dir = d
        self.coordList: list[tuple] = []

        if self.dir == Direction.NORTH:
            self.coordList = [(x, y - i) for i in range(0, self.len)]

        elif self.dir == Direction.WEST:
            self.coordList = [(x - i, y) for i in range(0, self.len)]

        elif self.dir == Direction.SOUTH:
            self.coordList = [(x, y + i) for i in range(0, self.len)]

        elif self.dir == Direction.EAST:
            self.coordList = [(x + i, y) for i in range(0, self.len)]

    def rotate(self):
        self.dir = self.dir.next

    def __str__(self):
        return "Location: :{}, len: {}, dir: {}\n".format(
            self.coordList, self.len, self.dir
        )

    def __repr__(self):
        return str(self)
