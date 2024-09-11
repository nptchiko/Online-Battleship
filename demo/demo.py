import pygame
import random
from abc import ABC

from itertools import zip_longest


class Ship:
    """Khởi tạo đối tượng ship để lưu vị trí"""

    def __init__(self, x, y, l):
        self.location = (x, y)
        self.length = l

    def __repr__(self):
        """In ra thông tin của tàu"""
        return "<Ship Object: ({},{}),  Length {}>".format(*self.location, self.length)


class Board(ABC):
    """Board là một đối tượng trừu tượng, sẽ được kế thừa bởi PlayerBoard và AIBoard"""

    def __init__(self, size=10, ship_sizes=[6, 4, 3, 3, 2]):
        self.size = size
        self.ship_sizes = ship_sizes
        self.ships_list = []
        self.hits_list = []
        self.misses_list = []

    def is_valid(self, ship):
        """Kiểm tra xem tọa độ tàu hiện tại có bị trùng với tàu nào không"""
        x, y = ship.location

        if x < 0 or y < 0 or x >= self.size or y >= self.size:
            return False

        for otherShip in self.ships_list:
            if self.ships_overlap(ship, otherShip):
                return False
        return True

    def add_ship(self, ship: Ship):
        """Thêm tàu vào list"""
        if self.is_valid(ship):
            self.ships_list.append(ship)
            return True
        else:
            return False

    def remove_ship(self, ship):
        """Xóa tàu khỏi Board khi không thể đặt tàu được hay tàu bị đánh chìm"""

        self.ships_list.remove(ship)

    def ships_overlap(self, ship1, ship2):
        if ship1.location == ship2.location:
            return True
        return False

    def get_ship(self, x, y):
        """Lấy tàu theo tọa độ x y đã cho"""
        for ship in self.ships_list:
            if (x, y) == ship.location:
                return ship
        return None

    def valid_target(self, x, y):
        """Kiểm tra liệu tọa độ phát bắn hiện tại có hợp lệ hay không

        Hợp lệ khi tọa độ nằm trong biên và chưa được đánh dấu
        """
        if x not in range(self.size) or y not in range(self.size):
            return False
        for previous_shot in self.misses_list + self.hits_list:
            if (x, y) == previous_shot:
                return False
        return True

    def shoot(self, x, y):
        """Thực hiện bắn tàu"""
        if not self.valid_target(x, y):
            return False

        """Nếu một tàu có tọa độ trùng với x y thì sẽ được thêm vào hit list và trả về"""

        for ship in self.ships_list:
            if (x, y) == ship.location:
                self.hits_list.append((x, y))
                return True

        """Thêm vào miss list"""
        self.misses_list.append((x, y))
        return True

    def colour_grid(self, colours, include_ships=True):
        """Tô màu cho Board dựa theo tọa độ tương ứng"""
        grid = [[colours["water"]
                 for _ in range(self.size)] for _ in range(self.size)]

        if include_ships:
            for ship in self.ships_list:
                x, y = ship.location
                grid[y][x] = colours["ship"]

        for x, y in self.hits_list:
            grid[y][x] = colours["hit"]

        for x, y in self.misses_list:
            grid[y][x] = colours["miss"]

        return grid

    @property
    def gameover(self):
        """Kiểm tra xem tọa độ các tàu trong list có nằm trong hit list hay không, nếu có thì trò chơi kết thúc"""
        for ship in self.ships_list:
            if ship.location not in self.hits_list:
                return False
        return True

    def __str__(self):
        """String representation of the board

        similar to colour grid but for printing
        """
        output = (("~" * self.size) + "\n") * self.size
        for ship in self.ships_list:
            x, y = ship.location
            output[x + y * (self.size + 1)] = "S"
        return output


class PlayerBoard(Board):
    """Phần giao diện bên người chơi, nằm ở trên"""

    def __init__(self, display, board_size, ship_sizes):
        """Yêu cầu người chơi chọn vị trí các tàu khi khởi tạo Board"""
        super().__init__(board_size, ship_sizes)
        self.display = display

        while True:
            self.display.show(None, self)

            if self.ship_to_place:
                text = "Hãy đặt vị trí tàu theo ý muốn: "
            else:
                text = "Nhấp bất kì đâu để bắt đầu!"
            self.display.show_text(text, lower=True)

            x, y = self.display.get_input()
            if x is not None and y is not None:
                ship = self.get_ship(x, y)
                if ship:
                    self.remove_ship(ship)
                    ship.rotate()
                    if self.is_valid(ship):
                        self.add_ship(ship)
                elif self.ship_to_place:
                    ship = Ship(x, y, self.ship_to_place)
                    if self.is_valid(ship):
                        self.add_ship(ship)
                else:
                    break

                if self.is_valid(ship):
                    self.add_ship(ship)

            Display.flip()

    @property
    def ship_to_place(self):
        placed_sizes = sorted(ship.length for ship in self.ships_list)
        sizes = sorted(self.ship_sizes)

        for placed, to_place in zip_longest(placed_sizes, sizes):
            if placed != to_place:
                return to_place
        return None


class AIBoard(Board):
    """Board của AI"""

    def __init__(self, board_size, ship_sizes):
        """Dùng random để gắn vị trí tàu của AI khi khởi tạo"""
        super().__init__(board_size, ship_sizes)
        for ship_length in self.ship_sizes:
            ship_added = False
            while not ship_added:
                x = random.randint(0, board_size - 1)
                y = random.randint(0, board_size - 1)
                ship = Ship(x, y, ship_length)
                if self.is_valid(ship):
                    self.add_ship(ship)
                    ship_added = True


class Display:
    """Đối tượng Display dùng để vẽ trò chơi lên màn hình"""

    """dic colours dùng để đánh màu các đối tượng trong game
        nước - xanh biển  
        tàu - xám  
        hit - đỏ
        miss - xanh nhạt  
        chữ - trắng
    """
    colours = {
        "water": pygame.color.Color("blue"),
        "ship": pygame.color.Color("gray"),
        "hit": pygame.color.Color("red"),
        "miss": pygame.color.Color("lightcyan"),
        "background": pygame.color.Color("navy"),
        "text": pygame.color.Color("white"),
    }

    def __init__(self, board_size=10, cell_size=30, margin=15):
        "Khởi tạo giao diện game bằng thư viện pygame"

        self.board_size = board_size
        self.cell_size = cell_size
        self.margin = margin

        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont("Helvetica", 14)

        screen_width = self.cell_size * board_size + 2 * margin
        screen_height = 2 * self.cell_size * board_size + 3 * margin
        self.screen = pygame.display.set_mode([screen_width, screen_height])
        pygame.display.set_caption("Battleships")

    def show(self, upper_board, lower_board, include_top_ships=False):
        """Vẽ các board lên màn hình tương ứng từng đối tượng
        Board trên - người chơi
        Board dưới - AI
        """
        if upper_board is not None:
            upper_colours = upper_board.colour_grid(
                self.colours, include_top_ships)

        if lower_board is not None:
            lower_colours = lower_board.colour_grid(self.colours)

        self.screen.fill(Display.colours["background"])

        """Vẽ màu từng ô trên màn hình theo đối tượng tương ứng"""
        for y in range(self.board_size):
            for x in range(self.board_size):
                if upper_board is not None:
                    pygame.draw.rect(
                        self.screen,
                        upper_colours[y][x],
                        [
                            self.margin + x * self.cell_size,
                            self.margin + y * self.cell_size,
                            self.cell_size,
                            self.cell_size,
                        ],
                    )

                if lower_board is not None:
                    offset = self.margin * 2 + self.board_size * self.cell_size
                    pygame.draw.rect(
                        self.screen,
                        lower_colours[y][x],
                        [
                            self.margin + x * self.cell_size,
                            offset + y * self.cell_size,
                            self.cell_size,
                            self.cell_size,
                        ],
                    )

    def get_input(self):
        """Lấy tọa độ con trỏ chuột khi người chơi nhấn chuột"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Display.close()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                y = y % (self.board_size * self.cell_size + self.margin)
                x = (x - self.margin) // self.cell_size
                y = (y - self.margin) // self.cell_size
                if x in range(self.board_size) and y in range(self.board_size):
                    return x, y
        return None, None

    def show_text(self, text, upper=False, lower=False):
        """Hiển thị chữ ra màn hình"""
        x = self.margin
        y_up = x
        y_lo = self.board_size * self.cell_size + self.margin
        label = self.font.render(text, True, Display.colours["text"])
        if upper:
            self.screen.blit(label, (x, y_up))
        if lower:
            self.screen.blit(label, (x, y_lo))

    @classmethod
    def flip(cls):
        pygame.display.flip()
        pygame.time.Clock().tick(60)

    @classmethod
    def close(cls):
        pygame.display.quit()
        pygame.quit()


class Game:
    """Đối tượng Game, quản lí các component của trò chơi"""

    def __init__(self, display, size=10, ship_sizes=[6, 4, 3, 3, 2]):
        """Set up game bằng khởi tạo 2 Board người chơi và AI"""
        self.display = display
        self.board_size = size
        self.ai_board = AIBoard(size, ship_sizes)
        self.player_board = PlayerBoard(display, size, ship_sizes)

    def play(self):
        """Vòng lặp chính trong game, cho đến khi game kết thúc"""
        print("Play starts")
        while not self.gameover:
            if self.player_shot():
                self.ai_shot()
            self.display.show(self.ai_board, self.player_board)
            self.display.show_text("Nhấp để đoán:")
            Display.flip()

    def ai_shot(self):
        """Dùng random để đoán vị trí tàu của người chơi"""
        x, y = -1, -1
        while not self.player_board.valid_target(x, y):
            x = random.randint(0, self.board_size - 1)
            y = random.randint(0, self.board_size - 1)
        self.player_board.shoot(x, y)

    def player_shot(self):
        """Kiểm tra xem input người chơi hợp lệ hay không"""
        x, y = self.display.get_input()
        if self.ai_board.valid_target(x, y):
            self.ai_board.shoot(x, y)
            return True
        else:
            return False

    @property
    def gameover(self):
        """In ra người thắng"""
        if self.ai_board.gameover:
            print("Chúc mừng bạn thắng")
            return True
        elif self.player_board.gameover:
            print("Bạn thua")
            return True
        else:
            return False


if __name__ == "__main__":
    while True:
        d = Display()
        Game(d).play()
        # Game(d, 2, [1,1]).play()
        d.close()

        response = input("Chơi lại y/n: ").lower()
        while response not in ["y", "n"]:
            response = input("Must be y or n: ")
        if response == "n":
            print("Thanks, goodbye.")
            break
