from tkinter import *
import random

S = [
        [
            "....",
            "..00",
            ".00.",
            "...."
        ],
        [
            "....",
            ".0..",
            ".00.",
            "..0."
        ]
    ]

Z = [
        [
            "....",
            ".00.",
            "..00",
            "...."
        ],
        [
            "....",
            "..0.",
            ".00.",
            ".0.."
        ]
    ]

I = [
        [
            "..0.",
            "..0.",
            "..0.",
            "..0."
        ],
        [
            "....",
            "0000",
            "....",
            "...."
        ]
    ]

T = [
        [
            "....",
            "..0.",
            ".000",
            "...."
        ],
        [
            "....",
            "..0.",
            ".00.",
            "..0."
        ],
        [
            "....",
            "....",
            ".000",
            "..0."
        ],
        [
            "....",
            "..0.",
            "..00",
            "..0."
        ],
    ]

O = [
        [
            "....",
            ".00.",
            ".00.",
            "....",
        ]
    ]

L = [
        [
            "....",
            ".0..",
            ".000",
            "...."
        ],
        [
            "....",
            ".00.",
            ".0..",
            ".0.."
        ],
        [
            "....",
            ".000",
            "...0",
            "...."
        ],
        [
            "....",
            "..0.",
            "..0.",
            ".00."
        ],
    ]

J = [
        [
            "....",
            "...0",
            ".000",
            "...."
        ],
        [
            "....",
            ".00.",
            "..0.",
            "..0."
        ],
        [
            "....",
            ".000",
            ".0..",
            "...."
        ],
        [
            "....",
            ".0..",
            ".0..",
            ".00."
        ],
    ]

shapes = [S, I, T, O, L, J, Z]
shape_color = ["red", "blue", "pink", "dark green", "purple", "orange", "black"]

class Pieces:
    def __init__(self, shape, x, y):
        self.x = x
        self.y = y
        self.color = shape_color[shapes.index(shape)]
        self.shape = shape
        self.rotation = 0

class Tetris(Canvas):
    state = False
    movable = False
    x = 0
    y = 1
    p = None

    def __init__(self, root):
        self.root = root
        self.width = 600
        super().__init__(root, bg="white")
        self.place(x=0, y=100, height=600, relwidth=1)
        self.tick = 500
        self.create_color_grid()

    def draw_lines(self):
        for y in range(20):
            self.create_line(0, y * 30, self.width, y * 30)
            self.create_line(y * 30, 0, y * 30, self.width)

    def spawn_shape(self, e=None):
        self.p = self.get_shape() if not e else e
        self.spawn(self.p)
        self.movable = True

    def game_tick(self):
        b = []
        
        if not self.movable:
            self.spawn_shape()
        if self.movable:
            pieces = self.find_withtag("fall")
            for piece in pieces:
                if self.movable:
                    self.move(piece, 0, 30 * self.y)
            self.p.y += self.y

        self.remove_tag(pieces)

        self.after(self.tick, self.game_tick)

    def remove_tag(self, pieces):
        if self.coords(pieces[-1])[-1] >= 600 and self.movable:
            self.movable = False
            self.dtag("fall", "fall")

            for piece in pieces:
                x, y = self.coords(piece)[0] // 30, self.coords(piece)[1] // 30
                x, y = int(x), int(y)
                print(x, y)
                self.main_grid[y][x] = self.p.color
            print(self.main_grid)

    def start_game(self, e):
        if not self.state:
            self.state = True
            self.after(self.tick, self.game_tick)
 
    def update_direction_press(self, e):
        if self.state:
            pieces = self.find_withtag("fall")
            if e.keysym == "Right":
                self.x = 1
                self.p.x += self.x
            if e.keysym == "Left":
                self.x = -1
                self.p.x += self.x
            if e.keysym == "space" and self.movable:
                dist = 600 - self.coords(pieces[-1])[-1]
                for piece in pieces:
                    self.move(piece, 0, dist)
                self.remove_tag(pieces)
                self.p.y = dist // 30
            if e.keysym == "Up":
                self.p.rotation = self.p.rotation + 1 if self.p.rotation < len(self.p.shape) - 1 else 0
                self.delete("fall")
                self.spawn_shape(self.p)

            for piece in pieces:
                if self.movable:
                    self.move(piece, 30 * self.x, 0)
    
    def update_direction_release(self, e):
        if e.keysym == "Right":
            self.x = 0
        if e.keysym == "Left":
            self.x = 0

    def spawn(self, p):
        formatted = self.decode_list(p)

        for pos in formatted:
            self.create_rectangle((pos[0] + p.x) * 30, (pos[1] + p.y) * 30, (pos[0] + p.x) * 30 + 30, (pos[1] + p.y) * 30 + 30, fill=p.color, tags=("fall"), outline=p.color)

    def decode_list(self, piece):
        pos = []
        no = piece.rotation % len(piece.shape)

        for i, col in enumerate(piece.shape[no]):
            for j, row in enumerate(col):
                if col[j] == "0":
                    pos.append([j, i])

        for p in pos:
            p[1] -= 4
            p[0] += 2

        return pos

    def create_color_grid(self):
        self.main_grid = [[0 for _ in range(20)] for _ in range(20)]
        print(self.main_grid)

    def get_shape(self):
        return Pieces(random.choice(shapes), 5, 0)

win = Tk()
win.title("Tetris")
win.resizable(False, False)
win.geometry("600x700")

game = Tetris(win)
game.draw_lines()

win.bind_all("<KeyRelease>", game.update_direction_release)
win.bind_all("<KeyPress>", game.update_direction_press)
win.bind_all("<e>", game.start_game)

win.mainloop()