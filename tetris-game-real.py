import pygame, random

colors = [
    "black",
    "orange",
    "red",
    "blue",
    "purple",
    "green",
    "cyan",
    "pink"
]


class Figure:
    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.figures) - 1)
        self.color = random.randint(1, len(colors) - 1)
        self.rotation = 0

    def image(self):
        return self.figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])


class Tetris:
    figure = None
    next_figure = None
    level = 2
    x = 0
    y = 0
    field = []
    height = 0
    width = 0
    block_size = 30
    breaks = 0
    state = "start"
    score = 1

    def __init__(self, height, width):
        self.next_figure = Figure(4, 0)
        self.height = height
        self.width = width
        self.field = []
        self.score = 1
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)
        self.state = "start"

    def new_figure(self):
        self.figure = self.next_figure
        self.next_figure = Figure(4, 0)

    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines ** 2
        self.breaks += lines ** 2

    def intersects(self) -> bool:
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[self.figure.y + i][self.figure.x + j] > 0:
                        intersection = True
        return intersection

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[self.figure.y + i][self.figure.x + j] = self.figure.color
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.state = "gameover"
        
    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation


pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("Tetris Theme.mp3")
pygame.mixer.music.play(-1)

height = 600
width = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

screen = pygame.display.set_mode((height, width))
done  = False
clock = pygame.time.Clock()
fps = 50
counter = 0
is_started = False
game = Tetris(20, 12)
pressed = False

while not done:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            done = True
        if e.type == pygame.KEYDOWN and is_started:
            if e.key == pygame.K_LEFT and game.state == "start":
                game.go_side(-1)
            if e.key == pygame.K_RIGHT and game.state == "start":
                game.go_side(1)
            if e.key == pygame.K_UP and game.state == "start":
                game.rotate()
            if e.key == pygame.K_SPACE and game.state == "start":
                game.go_space()
            if e.key == pygame.K_DOWN and game.state == "start":
                pressed = True
            if e.key == pygame.K_ESCAPE:
                pygame.mixer.music.stop()
                pygame.mixer.music.play(-1)
                game.__init__(20, 12)
        if e.type == pygame.KEYDOWN:
                is_started = True
        if e.type == pygame.KEYUP:
            if e.key == pygame.K_DOWN:
                pressed = False

    helvetica = pygame.font.SysFont("comicsans", 35, True, False)
    game_over = pygame.font.SysFont("comicsans", 55, False, False)

    if not is_started:
        screen.fill(WHITE)

        press = game_over.render("Press any key to start..", True, BLACK)
        screen.blit(press, [90, 250])

    elif is_started:
        if not game.figure:
            game.new_figure()
        counter += 1
        if counter > 100000:
            counter = 0

        if counter % (fps // game.level // 2) == 0 or pressed:
            if game.state == "start":
                game.go_down()

        screen.fill(WHITE)

        for i in range(game.height):
            for j in range(game.width):
                pygame.draw.rect(screen, BLACK, [game.x + game.block_size * j, game.y + game.block_size * i, game.block_size, game.block_size], 1)
                if game.field[i][j] > 0:
                    pygame.draw.rect(screen, colors[game.field[i][j]], [game.x + game.block_size * j, game.y + game.block_size * i, game.block_size, game.block_size])

        if game.figure is not None:
            for i in range(4):
                for j in range(4):
                    p = i * 4 + j
                    if p in game.figure.image():
                        pygame.draw.rect(screen, colors[game.figure.color],
                                        [game.x + game.block_size * (j + game.figure.x),
                                        game.y + game.block_size * (i + game.figure.y),
                                        game.block_size, game.block_size])
            for i in range(4):
                for j in range(4):
                    p = i * 4 + j
                    if p in game.next_figure.image():
                        pygame.draw.rect(screen, colors[game.next_figure.color], [420 + 30 * j, 90 + 30 * i, 30, 30])

            text_next_piece = helvetica.render("Next Piece", True, BLACK)
            screen.blit(text_next_piece, [410, 50])
            
            score = helvetica.render(f"Score :{game.score}", True, BLACK)
            screen.blit(score, [410, 300])

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
