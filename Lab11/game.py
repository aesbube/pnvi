import pygame
import random


pygame.init()

GRID_SIZE = 5
SQUARE_SIZE = 100
WIDTH = GRID_SIZE * SQUARE_SIZE
HEIGHT = GRID_SIZE * SQUARE_SIZE
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]  # 4 бои


def generate_board():
    board = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            available_colors = COLORS[:]
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and board[ny][nx]:
                    if board[ny][nx] in available_colors:
                        available_colors.remove(board[ny][nx])
            board[y][x] = random.choice(available_colors)
    return board


def draw_board():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            pygame.draw.rect(
                screen, board[row][col], (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.rect(screen, (0, 0, 0), (col * SQUARE_SIZE,
                             row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)


def fill_color(x, y):
    new_color = random.choice(COLORS)
    board[y][x] = new_color


def hasWon():
    squares = []
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            squares.append(str(board[x][y]))
    if len(set(squares)) == 1:
        return True
    return False


board = generate_board()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Color Fill Puzzle')

running = True
while running:
    screen.fill((255, 255, 255))
    draw_board()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if hasWon():
            print("You won!")
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            x = x // SQUARE_SIZE
            y = y // SQUARE_SIZE
            fill_color(x, y)

    pygame.display.flip()

pygame.quit()
